CREATE TABLE USER (
	email VARCHAR(255),
    record_confirmed BOOLEAN NOT NULL,
    record_fatalities BOOLEAN NOT NULL,
    top_5_most_confirmed BOOLEAN NOT NULL,
    top_5_most_fatalities BOOLEAN NOT NULL,
    population_pct BOOLEAN NOT NULL,
    top_5_least_confirmed BOOLEAN NOT NULL,
    top_5_least_fatalities BOOLEAN NOT NULL,
    total_fatalities_highest BOOLEAN NOT NULL,
    total_confirmed_highest BOOLEAN NOT NULL,
    notification_time TIME,
	PRIMARY KEY (email)
);
