-- PostgreSQL schema for Parents Poll MVP setup tables
-- This file creates the core structure for categories, blocks, questions, and options

-- ========================
-- Drop existing tables
-- ========================
DROP TABLE IF EXISTS options CASCADE;
DROP TABLE IF EXISTS questions CASCADE;
DROP TABLE IF EXISTS blocks CASCADE;
DROP TABLE IF EXISTS categories CASCADE;
DROP TABLE IF EXISTS soundtracks CASCADE;

-- ========================
-- Categories
-- ========================
CREATE TABLE categories (
    id SERIAL PRIMARY KEY,
    category_name VARCHAR(100) NOT NULL,
    category_text TEXT,
    version VARCHAR(20),
    uuid TEXT UNIQUE
);

-- Indexes
CREATE INDEX idx_categories_name ON categories(category_name);
CREATE INDEX idx_categories_version ON categories(version);

-- ========================
-- Blocks
-- ========================
CREATE TABLE blocks (
    id SERIAL PRIMARY KEY,
    category_id INTEGER NOT NULL,
    category_name VARCHAR(100),
    block_number INTEGER NOT NULL,
    block_code VARCHAR(50) UNIQUE NOT NULL,
    block_text TEXT NOT NULL,
    version VARCHAR(20),
    uuid TEXT UNIQUE,
    CONSTRAINT unique_block_per_category UNIQUE (category_id, block_number)
);

-- Indexes
CREATE INDEX idx_blocks_category_id ON blocks(category_id);
CREATE INDEX idx_blocks_category_name ON blocks(category_name);
CREATE INDEX idx_blocks_number ON blocks(block_number);
CREATE INDEX idx_blocks_code ON blocks(block_code);
CREATE INDEX idx_blocks_version ON blocks(version);

-- ========================
-- Questions
-- ========================
CREATE TABLE questions (
    id SERIAL PRIMARY KEY,
    question_code VARCHAR(50) UNIQUE NOT NULL,
    question_number INTEGER NOT NULL,
    question_text TEXT NOT NULL,
    category_id INTEGER NOT NULL,
    category_name VARCHAR(100),
    is_start_question BOOLEAN DEFAULT FALSE,
    parent_question_id INTEGER,
    check_box BOOLEAN DEFAULT FALSE,
    max_select INTEGER DEFAULT 1,
    block_number INTEGER NOT NULL,
    block_text TEXT,
    color_code TEXT,
    version VARCHAR(20)
);

-- Indexes
CREATE INDEX idx_questions_code ON questions(question_code);
CREATE INDEX idx_questions_number ON questions(question_number);
CREATE INDEX idx_questions_category_id ON questions(category_id);
CREATE INDEX idx_questions_category_name ON questions(category_name);
CREATE INDEX idx_questions_block_number ON questions(block_number);
CREATE INDEX idx_questions_start ON questions(is_start_question);
CREATE INDEX idx_questions_parent ON questions(parent_question_id);
CREATE INDEX idx_questions_version ON questions(version);

-- ========================
-- Options
-- ========================
CREATE TABLE options (
    id SERIAL PRIMARY KEY,
    category_id INTEGER NOT NULL,
    category_name VARCHAR(100),
    block_number INTEGER NOT NULL,
    block_text TEXT NOT NULL,
    question_code VARCHAR(50) NOT NULL,
    question_number INTEGER NOT NULL,
    question_text TEXT NOT NULL,
    check_box BOOLEAN DEFAULT FALSE,
    max_select INTEGER DEFAULT 1,
    option_select VARCHAR(10) NOT NULL,
    option_code VARCHAR(50) NOT NULL,
    option_text TEXT NOT NULL,
    response_message TEXT,
    companion_advice TEXT,
    tone_tag TEXT,
    next_question_id INTEGER,
    version VARCHAR(20),
    CONSTRAINT unique_option_per_question UNIQUE (question_code, option_select)
);

-- Indexes
CREATE INDEX idx_options_category_id ON options(category_id);
CREATE INDEX idx_options_category_name ON options(category_name);
CREATE INDEX idx_options_block_number ON options(block_number);
CREATE INDEX idx_options_question_code ON options(question_code);
CREATE INDEX idx_options_question_number ON options(question_number);
CREATE INDEX idx_options_option_select ON options(option_select);
CREATE INDEX idx_options_option_code ON options(option_code);
CREATE INDEX idx_options_version ON options(version);

-- ========================
-- Soundtracks
-- ========================
CREATE TABLE soundtracks (
    id SERIAL PRIMARY KEY,
    song_id VARCHAR(50) UNIQUE NOT NULL,
    song_title VARCHAR(255) NOT NULL,
    mood_tag TEXT,
    playlist_tag TEXT,
    lyrics_snippet TEXT,
    featured BOOLEAN DEFAULT FALSE,
    featured_order INTEGER DEFAULT 0,
    file_url TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Indexes
CREATE INDEX idx_soundtracks_featured ON soundtracks(featured, featured_order);
CREATE INDEX idx_soundtracks_playlist ON soundtracks USING GIN(to_tsvector('english', playlist_tag));
CREATE INDEX idx_soundtracks_mood ON soundtracks USING GIN(to_tsvector('english', mood_tag));
