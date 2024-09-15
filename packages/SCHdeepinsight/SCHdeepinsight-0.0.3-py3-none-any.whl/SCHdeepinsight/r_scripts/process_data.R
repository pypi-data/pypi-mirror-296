# File: process_data.R

process_and_project_data <- function(input_file, ref_file, output_prefix) {
  # Check for necessary libraries
  required_packages <- c("zellkonverter", "Seurat", "SeuratDisk", "ProjecTILs", "Matrix", "data.table")

  missing_packages <- required_packages[!(required_packages %in% installed.packages()[,"Package"])]

  if (length(missing_packages) > 0) {
      stop(paste("The following required packages are missing. Please install them before running this script:", 
                 paste(missing_packages, collapse = ", ")))
  }

  # Load the required packages
  lapply(required_packages, require, character.only = TRUE)

  # Read the .h5ad file
  adata <- readH5AD(input_file)
  
  # Use raw data if available
  if (!is.null(adata$raw)) {
    adata$X <- assay(adata$raw)
  }
  
  # Set feature_name if not present
  if (!"feature_name" %in% colnames(rowData(adata))) {
    rowData(adata)$feature_name <- rownames(rowData(adata))
  }
  
  # Convert to Seurat object
  seurat_data <- CreateSeuratObject(counts = assay(adata), 
                                    meta.data = as.data.frame(colData(adata)))
  
  # Normalize data using sctransform
  seurat_data <- SCTransform(object = seurat_data, verbose = FALSE)
  
  # Project using ProjecTILs
  reference <- readRDS(ref_file)
  query_projected <- Run.ProjecTILs(seurat_data, ref = reference, filter.cell = FALSE, skip.normalize = TRUE)
  
  # Adjust expression values before saving
  query_raw <- assay(adata)
  
  # Align gene order
  query_raw <- query_raw[rownames(query_projected), ]
  
  # Extract projected data
  query_df <- GetAssayData(query_projected)
  
  # Replace zero values
  query_df[query_raw == 0] <- 0
  
  # Update the projected object with the adjusted data
  query_projected <- SetAssayData(query_projected, new.data = query_df)
  
  # Save as .h5seurat and convert to .h5ad
  SaveH5Seurat(query_projected, paste0(output_prefix, ".h5seurat"))
  Convert(paste0(output_prefix, ".h5seurat"), dest = "h5ad")
}
