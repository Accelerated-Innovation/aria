-- Script to update pgvector dimensions to 3072 for text-embedding-3-large model

-- Connect to the database
\c aria_db;

-- First, check if the pgvector extension is installed
CREATE EXTENSION IF NOT EXISTS vector;

-- Drop existing tables that use the vector type if they exist
DROP TABLE IF EXISTS aria_pg_embedding CASCADE;

-- Recreate the collection table with Aria-specific naming
CREATE TABLE IF NOT EXISTS aria_pg_collection (
    uuid UUID PRIMARY KEY,
    name TEXT NOT NULL,
    cmetadata JSONB
);

-- Create the embedding table with Aria-specific naming and correct vector dimension
CREATE TABLE aria_pg_embedding (
    id UUID PRIMARY KEY,
    collection_id UUID NOT NULL REFERENCES aria_pg_collection(uuid) ON DELETE CASCADE,
    embedding vector(3072) NOT NULL,  -- Set to 3072 dimensions for text-embedding-3-large
    document TEXT,
    cmetadata JSONB,
    custom_id TEXT
);

-- Create an index using halfvec type which supports high dimensions
-- This converts the vector to halfvec type for indexing purposes
CREATE INDEX ON aria_pg_embedding USING hnsw((embedding::halfvec(3072)) halfvec_cosine_ops);

-- Grant permissions
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO aria_user;

-- Output confirmation
\echo 'Vector database updated to 3072 dimensions with Aria-specific table names using halfvec indexing';
