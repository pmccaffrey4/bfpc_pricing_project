-- Rename price_two_dogs_same_kennel column to price_additional_dog
ALTER TABLE kennel_suites 
RENAME COLUMN price_two_dogs_same_kennel TO price_additional_dog;

-- Add dog_sizes column as JSONB and migrate existing data
ALTER TABLE kennel_suites 
ADD COLUMN dog_sizes JSONB;

-- Fill dog_sizes with data from dog_size column formatted as a JSON array
UPDATE kennel_suites 
SET dog_sizes = jsonb_build_array(dog_size)
WHERE dog_sizes IS NULL AND dog_size IS NOT NULL;

-- Make dog_sizes column NOT NULL once data is migrated
ALTER TABLE kennel_suites 
ALTER COLUMN dog_sizes SET NOT NULL;

-- Optional: Drop the old dog_size column (only if you're sure the migration worked properly)
-- ALTER TABLE kennel_suites DROP COLUMN dog_size;
