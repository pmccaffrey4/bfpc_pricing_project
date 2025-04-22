-- Day Camp Daily Options Table
CREATE TABLE daycamp_daily (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    center_name TEXT NOT NULL,
    district_manager TEXT NOT NULL,
    full_address TEXT,
    dropin DECIMAL(10, 2) NOT NULL,
    halfday DECIMAL(10, 2) NOT NULL,
    weekend DECIMAL(10, 2) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT now(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT now()
);

-- Enable Row Level Security
ALTER TABLE daycamp_daily ENABLE ROW LEVEL SECURITY;

-- Create updated_at trigger
CREATE OR REPLACE FUNCTION update_modified_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = now();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER update_daycamp_daily_updated_at
BEFORE UPDATE ON daycamp_daily
FOR EACH ROW
EXECUTE FUNCTION update_modified_column();
