export type AppViewMode = 'overview' | 'observations' | 'change' | 'swipe' | 'ml';

export interface LayerOption {
  id: string;
  name: string;
  category: 'backscatter' | 'difference' | 'classified' | 'mask' | 'ml';
  cycle?: string;
  pol?: string;
  date?: string;
  baseline?: string;
  target?: string;
  filtered?: boolean;
}

export interface BoundsMetadata {
  center: [number, number];
  zoom: number;
  coordinates: [number, number][];
  bbox: [number, number, number, number];
  epsg: string;
  area_km2: number;
  dimensions: [number, number];
  resolution_m: number;
}

export interface Acquisition {
  cycle: string;
  date: string;
  orbit: string;
  direction: string;
}

export interface MetadataResponse {
  study_area: string;
  bounds: BoundsMetadata;
  acquisitions: Acquisition[];
  raster_metadata: Record<string, any>;
}

export interface BandStat {
  min: number;
  max: number;
  mean: number;
  std: number;
}

export interface ReportItem {
  id: string;
  filename: string;
  title: string;
}

export interface MLStatus {
  available: boolean;
  files_ready: {
    cluster_map: boolean;
    model_metadata: boolean;
    cluster_statistics: boolean;
  };
}

export interface ClusterCentroidData {
  id: number;
  interpretation: string;
  pixel_count: number;
  area_percentage: number;
  feature_centroids_db: {
    hh_028_db: number;
    hh_032_db: number;
    hh_033_db: number;
    hv_028_db: number;
    hv_032_db: number;
    hv_033_db: number;
    hh_diff_028_032: number;
    hh_diff_032_033: number;
    hh_diff_028_033: number;
    hv_diff_028_032: number;
    hv_diff_032_033: number;
    hv_diff_028_033: number;
  };
}

export interface MLSummaryData {
  centroids?: Record<string, ClusterCentroidData>;
  statistics?: Record<string, any>;
  metadata?: Record<string, any>;
}

export interface ChangeRegionProperties {
  id: string;
  polarization: string;
  baseline: string;
  target: string;
  interval: string;
  category: string;
  confidence: string;
  mean_diff_db: number;
  pixel_count: number;
  area_ha: number;
  interpretation: string;
  limitations: string;
}

export interface RegionSummaryItem {
  pol: string;
  interval: string;
  pair: string;
  total_regions: number;
  total_area_ha: number;
  significant_decreases: number;
  significant_increases: number;
}
