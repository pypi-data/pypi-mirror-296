CREATE TRIGGER IF NOT EXISTS after_prediction_insert
    AFTER INSERT ON Prediction
    FOR EACH ROW
    BEGIN
        DECLARE v_correction_factor FLOAT;
        DECLARE v_avg_correction_error FLOAT;
        DECLARE v_avg_last_n_corrections FLOAT;

        SELECT correction_factor, avg_correction_error, avg_last_n_corrections
        INTO v_correction_factor, v_avg_correction_error, v_avg_last_n_corrections
        FROM TrainedModel
        WHERE chain = NEW.chain AND feed = NEW.feed AND name = NEW.name
        ORDER BY timestamp DESC
        LIMIT 1;

        INSERT INTO Evaluation (id, chain, voting_round, feed, name, prediction, correction_factor, avg_correction_error, avg_last_n_corrections, timestamp)
        VALUES (
            UUID(),
            NEW.chain,
            NEW.voting_round,
            NEW.feed,
            NEW.name,
            NEW.prediction,
            v_correction_factor,
            v_avg_correction_error,
            v_avg_last_n_corrections,
            NEW.timestamp
        )
        ON DUPLICATE KEY UPDATE
            prediction = NEW.prediction,
            correction_factor = v_correction_factor,
            avg_correction_error = v_avg_correction_error,
            avg_last_n_corrections = v_avg_last_n_corrections,
            timestamp = NEW.timestamp;
    END;