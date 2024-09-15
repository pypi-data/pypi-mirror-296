DELIMITER $$

CREATE PROCEDURE SPEvaluationResults(
    IN input_name VARCHAR(255),
    IN input_limit INT
)
BEGIN
    SELECT
        voting_round,
        name,
        prediction,
        price,
        correction_factor,
        prediction + correction_factor + avg_last_n_corrections AS revised_prediction,
        avg_last_n_corrections,
        price - (prediction + correction_factor + avg_last_n_corrections) AS diff,
        price - prediction AS start_diff
    FROM Evaluation
    WHERE name = input_name
      AND correction_factor IS NOT NULL
    ORDER BY voting_round DESC
    LIMIT input_limit;
END $$

DELIMITER ;
