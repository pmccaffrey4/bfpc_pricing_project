-- Centers/Locations Table
CREATE TABLE centers (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    ctr_cd TEXT,
    ctr_name TEXT NOT NULL,
    is_open BOOLEAN DEFAULT true,
    is_acquisition BOOLEAN DEFAULT false,
    full_address TEXT,
    city TEXT,
    state TEXT,
    zipcode TEXT,
    nelson_dma TEXT,
    dma_code TEXT,
    district_manager TEXT NOT NULL,
    market_manager TEXT,
    center_manager TEXT,
    crm_email TEXT,
    services TEXT,
    system TEXT,
    website TEXT,
    google_ads_account TEXT,
    google_ads_reports_links TEXT,
    active BOOLEAN DEFAULT true,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT now(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT now()
);

-- Enable Row Level Security
ALTER TABLE centers ENABLE ROW LEVEL SECURITY;

-- Create updated_at trigger
CREATE TRIGGER update_centers_updated_at
BEFORE UPDATE ON centers
FOR EACH ROW
EXECUTE FUNCTION update_modified_column();
