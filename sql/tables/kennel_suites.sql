-- Boarding Kennel Suites Table
CREATE TABLE kennel_suites (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    center_name TEXT NOT NULL,
    district_manager TEXT NOT NULL,
    full_address TEXT,
    suite_name TEXT NOT NULL,
    dog_size TEXT NOT NULL,
    price_per_night DECIMAL(10, 2) NOT NULL,
    price_two_dogs_same_kennel DECIMAL(10, 2),
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
