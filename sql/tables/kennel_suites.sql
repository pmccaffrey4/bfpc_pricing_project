-- Drop existing table if it exists (CAUTION: This will delete all data!)
DROP TABLE IF EXISTS kennel_suites CASCADE;

-- Boarding Kennel Suites Table
CREATE TABLE kennel_suites (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    center_name TEXT NOT NULL,
    district_manager TEXT NOT NULL,
    full_address TEXT,
    suite_name TEXT NOT NULL,
    dog_sizes JSONB NOT NULL, -- JSONB array to store multiple dog sizes
    price_per_night DECIMAL(10, 2) NOT NULL,
    price_additional_dog DECIMAL(10, 2), -- Price for an additional dog in the same kennel
    num_kennels INTEGER NOT NULL,
    features JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT now(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT now()
);

-- Enable Row Level Security
ALTER TABLE kennel_suites ENABLE ROW LEVEL SECURITY;

-- Create updated_at trigger
CREATE TRIGGER update_kennel_suites_updated_at
BEFORE UPDATE ON kennel_suites
FOR EACH ROW
EXECUTE FUNCTION update_modified_column();
