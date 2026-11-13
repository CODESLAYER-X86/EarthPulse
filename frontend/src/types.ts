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
