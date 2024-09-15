import os
from pathlib import Path
import anndata
import pandas as pd
import numpy as np
import scanpy as sc
from scipy.sparse import issparse
import torch
from torch import nn
from torchvision import transforms
from PIL import Image
from torch.utils.data import Dataset
from efficientnet_pytorch import EfficientNet
import pickle
from sklearn import preprocessing
import cv2
from pyDeepInsight import ImageTransformer
import warnings
import torch.nn.functional as F
import rpy2.robjects as ro

warnings.filterwarnings("ignore")

class Immune:
    def __init__(self):
        self.pretrained_dir = Path(__file__).resolve().parent / "pretrained_files_immune"
        self.gene_list = self._load_gene_list()
        self.img_transformer = self._load_img_transformer()
        self.index = [8, 2, 11, 2, 2, 4, 4, 1, 5, 3, 3, 1, 2, 1, 1]
        self.model = self._load_model()

    def _load_gene_list(self):
        gene_list_path = self.pretrained_dir / "pretrained_genes_immune.csv"
        if not gene_list_path.exists():
            raise FileNotFoundError(f"Gene list file not found at {gene_list_path}")
        return pd.read_csv(gene_list_path, index_col=0).index.tolist()

    def _load_img_transformer(self):
        transformer_path = self.pretrained_dir / "img_transformer_immune.obj"
        if not transformer_path.exists():
            raise FileNotFoundError(f"Image transformer file not found at {transformer_path}")
        with open(transformer_path, 'rb') as file:
            return pickle.load(file)

    def _load_model(self):
        model = EfficientNet.from_pretrained('efficientnet-b4', num_classes=50)
        model = nn.DataParallel(model)
        checkpoint_path = self.pretrained_dir / "checkpoint_model_immune.pth"
        if not checkpoint_path.exists():
            raise FileNotFoundError(f"Model checkpoint not found at {checkpoint_path}")
        if torch.cuda.is_available():
            model.load_state_dict(torch.load(checkpoint_path), strict=False)
        else:
            model.load_state_dict(torch.load(checkpoint_path, map_location=torch.device('cpu')), strict=False)
        return model.to(torch.device("cuda:0" if torch.cuda.is_available() else "cpu")).eval()

    def batch_correction(self, input_file, ref_file, output_prefix):
        """Performs batch correction using an R script for data projection."""
        # Create the output directory
        os.makedirs(output_prefix, exist_ok=True)

        # Read and preprocess the .h5ad file
        query = anndata.read_h5ad(input_file)

        # Check if raw data exists and use it
        if query.raw is not None:
            query.X = query.raw.X

        # Ensure "feature_name" is present
        if "feature_name" not in query.var.columns:
            query.var["feature_name"] = query.var.index.tolist()

        # Write barcodes.tsv
        barcodes_path = os.path.join(output_prefix, 'barcodes.tsv')
        with open(barcodes_path, 'w') as f:
            for item in query.obs_names:
                f.write(item + '\n')

        # Write features.tsv
        features_path = os.path.join(output_prefix, 'features.tsv')
        with open(features_path, 'w') as f:
            for item in ['\t'.join([x, x, 'Gene Expression']) for x in query.var["feature_name"]]:
                f.write(item + '\n')

        # Write matrix.mtx
        matrix_path = os.path.join(output_prefix, 'matrix.mtx')
        io.mmwrite(matrix_path, query.X.T)

        # Gzip the matrix files
        os.system(f'gzip {output_prefix}/*')

        # Write metadata.csv
        metadata_path = os.path.join(output_prefix, 'metadata.csv')
        query.obs.to_csv(metadata_path)

        # Get the path to the R script
        script_dir = Path(__file__).resolve().parent
        r_script_path = script_dir / 'r_scripts' / 'process_data.R'
        
        # Load the R script
        r = ro.r
        r.source(str(r_script_path))
        
        # Call the R function
        process_r = ro.globalenv['process_and_project_data']
        process_r(output_prefix, ref_file)

    def preprocess(self, query_path: str, output_path: str):
        """Performs normalization and log1p transformation on the input .h5ad file."""
        query = anndata.read_h5ad(query_path)
        sc.pp.normalize_per_cell(query)
        sc.pp.log1p(query)
        query.write(output_path)  # Save the preprocessed .h5ad file
        return query

    def image_transform(self, query_path: str, barcode_path: str, image_path: str):
        """Transforms the .h5ad file into a DataFrame and then into images."""
        query = anndata.read_h5ad(query_path)
        query.var["feature_name"] = query.var.get("feature_name", query.var.index.tolist())
        query.var.index = query.var["feature_name"].values

        remain_list = list(set(query.var.index) & set(self.gene_list))
        query = query[:, remain_list]

        sample = self._scale_and_fill(query)
        self._save_barcode(sample, barcode_path)
        self._save_image(sample, image_path)

    def predict(self, barcode_path: str, image_path: str, batch_size: int = 128):
        """Predicts cell types and identifies potential rare cells."""
        class MyTestSet(Dataset):
            def __init__(self, img):
                self.img = np.load(img)
                self.transforms = transforms.Compose([transforms.ToTensor(), ])
            def __getitem__(self, index):
                img = self.img[index, :, :, :]
                img = np.squeeze(img)
                img = Image.fromarray(np.uint8(img))
                img = self.transforms(img)
                return img
            def __len__(self):
                return self.img.shape[0]

        test_set = MyTestSet(image_path)
        test_loader = torch.utils.data.DataLoader(test_set, batch_size=batch_size, shuffle=False)

        device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
        self.model.to(device)

        out_base, out_detailed, out_base_probs, out_detailed_probs = [], [], [], []

        for data in test_loader:
            query = data.to(device)
            pred = F.softmax(self.model(query), dim=1)

            # Step 1: Determine base type through summing subtype probabilities
            base_tensor = self._sum_base_type_tensor(pred.data)
            base_probs, predicted_base_by_tree = torch.max(base_tensor, 1)

            # Step 2: Only consider the probabilities of the subtypes corresponding to the predicted base type
            output_sub = self._sub_predicted(pred.data, predicted_base_by_tree)

            # Set the probabilities of subtypes not belonging to the predicted base type to 0
            for i in range(len(output_sub)):
                base_type = predicted_base_by_tree[i].item()
                k1 = sum(self.index[:base_type])
                k2 = sum(self.index[:base_type + 1])
                output_sub[i, :k1] = 0  # Mask probabilities of subtypes not belonging to the base type
                output_sub[i, k2:] = 0  # Mask probabilities of subtypes not belonging to the base type

            # Finally, select the detailed subtype
            detail_probs, predicted_detailed = torch.max(output_sub.data, 1)

            out_base.append(predicted_base_by_tree)
            out_detailed.append(predicted_detailed)
            out_base_probs.append(base_probs)
            out_detailed_probs.append(detail_probs)

        # Create DataFrame with predictions
        pred_label = self._create_pred_label(barcode_path, out_base, out_detailed, out_base_probs, out_detailed_probs)

        # Determine potential rare cells
        pred_label['is_potential_rare'] = pred_label.groupby('predicted_base_type', group_keys=False).apply(self._is_potential_rare)

        return pred_label

    def _scale_and_fill(self, query):
        if issparse(query.X):
            sample = pd.DataFrame(query.X.toarray()).T
        else:
            sample = pd.DataFrame(query.X).T
        sample = preprocessing.MinMaxScaler().fit_transform(sample)
        sample = pd.DataFrame(sample).T
        sample.index = query.obs.index.values
        sample.columns = query.var.index.values

        excluded_genes = list(set(self.gene_list) - set(sample.columns))
        blank_dataframe = pd.DataFrame(np.zeros((len(sample), len(excluded_genes))), 
                                       index=sample.index, columns=excluded_genes)
        sample = pd.concat([sample, blank_dataframe], axis=1)
        sample = sample[self.gene_list]
        return sample

    def _save_barcode(self, sample, barcode_path):
        barcode = pd.DataFrame(sample.index.tolist(), columns=["barcode"])
        barcode.to_csv(barcode_path, index=False)

    def _save_image(self, sample, image_path):
        query_img = cv2.normalize(self.img_transformer.transform(sample.values), None, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX)
        query_img = query_img.astype(np.uint8)
        np.save(image_path, query_img)

    def _sum_base_type_tensor(self, data):
        base_type_tensor = torch.sum(data[:, 0:self.index[0]], dim=1).expand(1, -1)
        for i in range(1, len(self.index)):
            k1 = sum(self.index[0:i])
            k2 = sum(self.index[0:i+1])
            base_type_tensor = torch.cat(
                (base_type_tensor, torch.sum(data[:, k1:k2], dim=1).expand(1, -1)), dim=0
            )
        return base_type_tensor.t()

    def _sub_predicted(self, output, predicted_base_type):
        sub_tensor = output.clone()
        for i in range(len(sub_tensor)):
            base_type = predicted_base_type[i]
            k1 = sum(self.index[0:base_type])
            k2 = sum(self.index[0:base_type + 1])
            sub_tensor[i, :k1] = 0
            sub_tensor[i, k2:] = 0
        return sub_tensor

    def _create_pred_label(self, barcode_path, out_base, out_detailed, out_base_probs, out_detailed_probs):
        pred_base = torch.cat(out_base).cpu().numpy()
        pred_detailed = torch.cat(out_detailed).cpu().numpy()
        pred_base_probs = torch.cat(out_base_probs).cpu().numpy()
        pred_detail_probs = torch.cat(out_detailed_probs).cpu().numpy()

        pred_label_base = self._decode_labels(pred_base, "label_encoder_immune_base.obj", "predicted_base_type")
        pred_label_detailed = self._decode_labels(pred_detailed, "label_encoder_immune_detailed.obj", "predicted_detailed_type")

        labels_prob = pd.DataFrame({
            "predicted_base_type_prob": pred_base_probs,
            "predicted_detailed_type_prob": pred_detail_probs
        })

        barcode = pd.read_csv(barcode_path)
        return pd.concat([barcode["barcode"], pred_label_base, pred_label_detailed, labels_prob], axis=1)

    def _decode_labels(self, predictions, encoder_file, column_name):
        encoder_path = self.pretrained_dir / encoder_file
        if not encoder_path.exists():
            raise FileNotFoundError(f"Label encoder not found at {encoder_path}")
        with open(encoder_path, 'rb') as file:
            encoder = pickle.load(file)
        labels = encoder.inverse_transform(predictions)
        return pd.DataFrame(labels, columns=[column_name])

    def _is_potential_rare(self, base_type_group):
        base_prob_50th = np.percentile(base_type_group['predicted_base_type_prob'], 50)
        detailed_prob_20th = np.percentile(base_type_group['predicted_detailed_type_prob'], 20)
        return (base_type_group['predicted_base_type_prob'] > base_prob_50th) & \
               (base_type_group['predicted_detailed_type_prob'] < detailed_prob_20th)
