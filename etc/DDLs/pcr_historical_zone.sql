DELIMITER //

CREATE PROCEDURE historical_zone(pickup_place TEXT, month_query TEXT )
BEGIN

	SELECT	month_query, hs.rank_id, hs.pick_up, hs.drop_off
	FROM 	historical_zones hs
	JOIN 	(	SELECT	MAX(month_id) as month_id, rank_id, pick_up
				FROM 	historical_zones
				WHERE 	pick_up = pickup_place
				AND 	STR_TO_DATE(concat(month_id, "-01"), "%Y-%m-%d") <= month_query
				GROUP 	BY rank_id, pick_up) control
	ON 		hs.month_id = control.month_id
	AND 	hs.rank_id = control.rank_id
	AND 	hs.pick_up = control.pick_up
	ORDER BY rank_id;

END; //

DELIMITER ;