CREATE TABLE bot_user(
    telegram_user_id BIGINT PRIMARY KEY,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL
);

CREATE TABLE data_text(
    data_text_id INTEGER PRIMARY KEY AUTOINCREMENT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    content VARCHAR(10000),
    telegram_user_id INT NOT NULL,
    FOREIGN KEY (telegram_user_id) REFERENCES user (telegram_user_id) ON DELETE CASCADE
);
