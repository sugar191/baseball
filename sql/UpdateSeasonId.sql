UPDATE player_common_records
INNER JOIN teams ON player_common_records.team_id = teams.id
INNER JOIN leagues ON teams.league_id = leagues.id
INNER JOIN seasons ON player_common_records.year = seasons.year
  AND leagues.organization_id = seasons.organization_id
SET player_common_records.season_id = seasons.id;

UPDATE player_batting_records
INNER JOIN player_common_records ON player_batting_records.player_id = player_common_records.player_id AND player_batting_records.year = player_common_records.year
INNER JOIN teams ON player_common_records.team_id = teams.id
INNER JOIN leagues ON teams.league_id = leagues.id
INNER JOIN seasons ON player_common_records.year = seasons.year
  AND leagues.organization_id = seasons.organization_id
SET player_batting_records.season_id = seasons.id;

UPDATE player_batting_records SET season_id = 289 WHERE YEAR = 9000;
UPDATE player_batting_records SET season_id = 290 WHERE YEAR = 9001;

UPDATE player_pitching_records
INNER JOIN player_common_records ON player_pitching_records.player_id = player_common_records.player_id AND player_pitching_records.year = player_common_records.year
INNER JOIN teams ON player_common_records.team_id = teams.id
INNER JOIN leagues ON teams.league_id = leagues.id
INNER JOIN seasons ON player_common_records.year = seasons.year
  AND leagues.organization_id = seasons.organization_id
SET player_pitching_records.season_id = seasons.id;

UPDATE player_pitching_records SET season_id = 289 WHERE YEAR = 9000;
UPDATE player_pitching_records SET season_id = 290 WHERE YEAR = 9001;

UPDATE player_fielding_records
INNER JOIN player_common_records ON player_fielding_records.player_id = player_common_records.player_id AND player_fielding_records.year = player_common_records.year
INNER JOIN teams ON player_common_records.team_id = teams.id
INNER JOIN leagues ON teams.league_id = leagues.id
INNER JOIN seasons ON player_common_records.year = seasons.year
  AND leagues.organization_id = seasons.organization_id
SET player_fielding_records.season_id = seasons.id;

UPDATE player_fielding_records SET season_id = 289 WHERE YEAR = 9000;
UPDATE player_fielding_records SET season_id = 290 WHERE YEAR = 9001;

UPDATE player_titles
INNER JOIN player_common_records ON player_titles.player_id = player_common_records.player_id AND player_titles.year = player_common_records.year
INNER JOIN teams ON player_common_records.team_id = teams.id
INNER JOIN leagues ON teams.league_id = leagues.id
INNER JOIN seasons ON player_common_records.year = seasons.year
  AND leagues.organization_id = seasons.organization_id
SET player_titles.season_id = seasons.id;
