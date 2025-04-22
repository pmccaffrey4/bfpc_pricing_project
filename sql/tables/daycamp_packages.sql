-- Day Camp Packages Table
CREATE TABLE daycamp_packages (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    center_name TEXT NOT NULL,
    district_manager TEXT NOT NULL,
    full_address TEXT,
    days INTEGER NOT NULL,
    price DECIMAL(10, 2) NOT NULL,
    expiration TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT now(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT now()
);

-- Enable Row Level Security
ALTER TABLE daycamp_packages ENABLE ROW LEVEL SECURITY;

-- Create updated_at trigger
CREATE TRIGGER update_daycamp_packages_updated_at
BEFORE UPDATE ON daycamp_packages
FOR EACH ROW
EXECUTE FUNCTION update_modified_column();
