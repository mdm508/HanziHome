DROP TABLE IF EXISTS Etymology;
DROP TABLE IF EXISTS Characters;

CREATE TABLE IF NOT EXISTS Characters (
    hanzi TEXT PRIMARY KEY,
    definition TEXT,
    decomposition TEXT NOT NULL,
    radical TEXT NOT NULL,
    keyword TEXT,
    rth INTEGER,
    pinyin TEXT NOT NULL,
    ipa TEXT NOT NULL,
    zhuyin TEXT NOT NULL,
    matches TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS Etymology (
    hanzi TEXT NOT NULL,
    type TEXT NOT NULL,
    hint TEXT,
    phonetic TEXT,
    semantic TEXT,
    PRIMARY KEY (hanzi, type),
    FOREIGN KEY (hanzi) REFERENCES Characters(hanzi) ON DELETE CASCADE
);
