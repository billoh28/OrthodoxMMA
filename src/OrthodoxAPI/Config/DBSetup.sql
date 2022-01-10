--This file is for if the user wishes to setup locally, provides MYSQL Schema for the application

CREATE TABLE credentials (
    Email VARCHAR(255),
    Encrypt_pasword VARCHAR(255),
    PRIMARY KEY (Email)
);

CREATE TABLE feedbacks (
    Email VARCHAR(255),
    Feedback VARCHAR(255),
);