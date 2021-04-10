PRAGMA foreign_keys=on;

DROP TABLE IF EXISTS tribes;
CREATE TABLE IF NOT EXISTS tribes (
        id INTEGER PRIMARY KEY NOT NULL,
        name TEXT
        );


DROP TABLE IF EXISTS species;
CREATE TABLE IF NOT EXISTS species (
        id INTEGER PRIMARY KEY NOT NULL,
        name TEXT,
        common_names TEXT,
        usda_code TEXT,
        family TEXT,
        family_apg TEXT
        );

DROP TABLE IF EXISTS sources;
CREATE TABLE IF NOT EXISTS  sources(
        id INTEGER PRIMARY KEY NOT NULL,
        refcode TEXT,
        type TEXT,
        fulltext TEXT,
        address TEXT,
        author TEXT,
        booktitle TEXT,
        comment TEXT,
        edition TEXT,
        editor TEXT,
        journal TEXT,
        month TEXT,
        note TEXT,
        number TEXT,
        pages TEXT,
        publisher TEXT,
        school TEXT,
        title TEXT,
        url TEXT,
        volume TEXT,
        year TEXT
        );

DROP TABLE IF EXISTS use_categories;
CREATE TABLE IF NOT EXISTS use_categories (
        id INTEGER PRIMARY KEY NOT NULL,
        name TEXT
        );

DROP TABLE IF EXISTS use_subcategories;
CREATE TABLE IF NOT EXISTS use_subcategories (
        id INTEGER PRIMARY KEY NOT NULL,
        parent INTEGER, 
        name TEXT,
        FOREIGN KEY(parent) REFERENCES use_categories(id)
        );

DROP TABLE IF EXISTS uses;
CREATE TABLE IF NOT EXISTS uses (
        id INTEGER PRIMARY KEY NOT NULL,
        species INTEGER NOT NULL,
        tribe INTEGER NOT NULL,
        source INTEGER NOT NULL,
        rawsource TEXT NOT NULL,
        pageno TEXT NOT NULL,
        use_category INTEGER,
        use_subcategory INTEGER,
        notes TEXT,
        FOREIGN KEY(use_category) REFERENCES use_categories(id),
        FOREIGN KEY(use_subcategory) REFERENCES use_subcategories(id),
        FOREIGN KEY(tribe) REFERENCES tribe(id),
        FOREIGN KEY(species) REFERENCES species(id),
        FOREIGN KEY(source) REFERENCES sources(id)
        );
