import os
import view_sql.queries as q
from flask import Flask, render_template
from flask_mysql_connector import MySQL
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()
db_host = os.getenv("MYSQL_DATABASE_HOST")
db_port = os.getenv("MYSQL_DATABASE_PORT")
db_user =  os.getenv("MYSQL_DATABASE_USER")
db_pwd = os.getenv("MYSQL_DATABASE_PASSWORD")
db_name = os.getenv("MYSQL_DATABASE_DB")

app = Flask(__name__)
app.config["MYSQL_USER"] = db_user
app.config["MYSQL_PASSWORD"] = db_pwd
app.config["MYSQL_DATABASE"] = db_name
app.config["MYSQL_HOST"] = db_host

mysql = MySQL(app)

#  TODO FIX THE LEADING 0's!!!
#  TODO Batting Summary WAR looks like it is not summed

@app.route('/team/<team_id>')
def team_page(team_id):
    conn = mysql.connection
    cur = conn.cursor()
    cur.execute(q.team_roster(team_id))
    roster = cur.fetchall()
    cur.execute(q.team_name(team_id))
    team_name = cur.fetchall()
    results_dict = {}
    results_dict['roster'] = roster
    results_dict['team_name'] = team_name
    results_dict['team_id'] = team_id
    cur.execute(q.team_history_record(team_id))
    team_history_record = cur.fetchall()
    results_dict['team_history_record'] = team_history_record
    cur.execute(q.team_current_staff(team_id))
    team_current_staff = cur.fetchall()
    results_dict['current_staff'] = team_current_staff
    cur.execute(q.team_affiliates(team_id))
    affiliates = cur.fetchall()
    results_dict['affiliates'] = affiliates
    return render_template('team_main.html', results_dict=results_dict, team_id=team_id)

#  For team_year
def max_g_per_pos(team_id, year):
    positions = [2,3,4,5,6,7,8,9]
    starters = []
    conn = mysql.connection
    cur = conn.cursor()
    for position in positions:
        cur.execute(f"""
        SELECT b.player_id, b.g, p.position
        FROM CalcBatting b INNER JOIN players p ON b.player_id=p.player_id
        WHERE p.position = {position} AND b.team_id = {team_id} and b.year = {year}
        ORDER BY b.g desc
        LIMIT 1
        """)
        result = cur.fetchall()
        starters.append(result)
    return starters

@app.route('/team/<team_id>/<year>')
def team_year(team_id, year):
    results_dict = {}
    conn = mysql.connection
    cur = conn.cursor()
    cur.execute(q.team_name(team_id))
    team_name = cur.fetchall()
    results_dict['team_name'] = team_name
    starters = max_g_per_pos(team_id, year)
    results_dict['bat_starters'] = starters
    starter_ids = q.list_of_starters(starters)
    results_dict['bat_starter_ids'] = starter_ids
    if results_dict['bat_starter_ids'] == '()':
        cur.execute(q.team_year_all_batters(team_id, year))
        starter_batters = cur.fetchall()
        results_dict['bench_batters'] = starter_batters
    else:
        cur.execute(q.team_year_batters_starters(team_id, year, starter_ids))
        starter_batters = cur.fetchall()
        results_dict['starter_batters'] = starter_batters
        cur.execute(q.team_year_batters_bench(team_id, year, starter_ids))
        bench_batters = cur.fetchall()
        results_dict['bench_batters'] = bench_batters
    cur.execute(q.team_year_starting_p(team_id, year))
    starting_p_stats = cur.fetchall()
    results_dict['starting_p'] = starting_p_stats
    cur.execute(q.team_year_bullpen_p(team_id, year))
    bullpen_p_stats = cur.fetchall()
    results_dict['bullpen_p'] = bullpen_p_stats
    cur.execute(q.team_year_best_players(team_id, year))
    best_players = cur.fetchall()
    results_dict['best_players'] = best_players
    cur.execute(q.team_year_record(team_id, year))
    ty_record = cur.fetchall()
    results_dict['team_year_record'] = ty_record
    return render_template('team_year.html', results_dict=results_dict, year=year)


#  TODO Add retirement, retirement year, and turned coach to bio
@app.route('/player/<player_id>')
def player_page(player_id):
    results_dict = {}
    conn = mysql.connection
    cur = conn.cursor()
    cur.execute(q.player_bio(player_id))
    bio = cur.fetchall()
    results_dict['bio'] = bio
    cur.execute(q.player_major_bat_history_ovr(player_id))
    maj_bat_ovr = cur.fetchall()
    results_dict['maj_bat_ovr'] = maj_bat_ovr
    cur.execute(q.player_major_bat_history_VL(player_id))
    maj_bat_l = cur.fetchall()
    results_dict['maj_bat_l'] = maj_bat_l
    cur.execute(q.player_major_bat_history_VR(player_id))
    maj_bat_r = cur.fetchall()
    results_dict['maj_bat_r'] = maj_bat_r
    cur.execute(q.player_minors_bat_history_ovr(player_id))
    min_bat_ovr = cur.fetchall()
    results_dict['min_bat_ovr'] = min_bat_ovr
    cur.execute(q.player_minors_bat_history_VL(player_id))
    min_bat_l = cur.fetchall()
    results_dict['min_bat_l'] = min_bat_l
    cur.execute(q.player_minors_bat_history_VR(player_id))
    min_bat_r = cur.fetchall()
    results_dict['min_bat_r'] = min_bat_r
    cur.execute(q.player_major_pitch_history_ovr(player_id))
    maj_pitch_ovr = cur.fetchall()
    results_dict['maj_pitch_ovr'] = maj_pitch_ovr
    cur.execute(q.player_major_pitch_history_VL(player_id))
    maj_pitch_l = cur.fetchall()
    results_dict['maj_pitch_l'] = maj_pitch_l
    cur.execute(q.player_major_pitch_history_VR(player_id))
    maj_pitch_R = cur.fetchall()
    results_dict['maj_pitch_r'] = maj_pitch_R
    cur.execute(q.player_minor_pitch_history_ovr(player_id))
    min_pitch_ovr = cur.fetchall()
    results_dict['min_pitch_ovr'] = min_pitch_ovr
    cur.execute(q.player_minor_pitch_history_VL(player_id))
    min_pitch_l = cur.fetchall()
    results_dict['min_pitch_l'] = min_pitch_l
    cur.execute(q.player_minor_pitch_history_VR(player_id))
    min_pitch_R = cur.fetchall()
    results_dict['min_pitch_r'] = min_pitch_R
    cur.execute(q.player_career_bat_summary(player_id))
    career_bat_summary = cur.fetchall()
    results_dict['bat_summary'] = career_bat_summary
    cur.execute(q.player_career_pitch_summary(player_id))
    career_pitch_summary = cur.fetchall()
    results_dict['pitch_summary'] = career_pitch_summary
    return render_template('player.html', results_dict=results_dict)

@app.route('/league/<league_id>')
#  Current league information with link to history
def league(league_id):
    results_dict = {}
    conn = mysql.connection
    cur = conn.cursor()
    cur.execute(q.current_world_date())
    cur_date = cur.fetchone()
    year = cur_date[0].year
    world_date = cur_date[0].strftime("%B %d, %Y")
    cur.execute(q.get_affiliated_leagues())
    leagues = cur.fetchall()
    results_dict['leagues'] = leagues
    cur.execute(q.get_batting_stats_from_map())
    stats = cur.fetchall()
    cur.execute(q.get_divs_from_league(league_id))
    divisions = cur.fetchall()
#    divisions = [division[0] for division in divisions]
    div_records = {}
    #  BATTING STATS
    leaders_stats_b = {}
    for division in divisions:
        div_id = division[0]
        div_name = division[1]
        cur.execute(q.get_div_records(league_id,div_id))
        record = cur.fetchall()
        div_records[div_name] = record
        leaders_stats_b[div_name] = {}
        for stat in stats:
            cur.execute(q.get_current_league_bat_leaders(league_id, div_id, year, stat[2]))
            leader_stat_b = cur.fetchall()
            leaders_stats_b[div_name][stat[1]] = leader_stat_b
    #  PITCHING STATS
    cur.execute(q.get_current_pitch_stats_asc_from_map())
    pitch_stats_asc = cur.fetchall()
    cur.execute(q.get_current_pitch_stats_desc_from_map())
    pitch_stats_desc = cur.fetchall()
    leaders_stats_p = {}
    for division in divisions:
        div_id = division[0]
        div_name = division[1]
        leaders_stats_p[div_name] = {}
        for stat in pitch_stats_asc:
            cur.execute(q.get_current_pitch_leaders_asc(league_id,div_id,year,stat[2]))
            leader_stat_p = cur.fetchall()
            leaders_stats_p[div_name][stat[1]] = leader_stat_p
        for stat in pitch_stats_desc:
            cur.execute(q.get_current_pitch_leaders_desc(league_id, div_id, year, stat[2]))
            leader_stat_p = cur.fetchall()
            leaders_stats_p[div_name][stat[1]] = leader_stat_p
    cur.execute(q.get_league_info(league_id))
    info = cur.fetchall()
    return render_template('league.html', info=info, year=year, world_date=world_date, leaders_stats_p=leaders_stats_p, leaders_stats_b=leaders_stats_b, results_dict=results_dict, div_records=div_records, divisions=divisions)
#  NOTE that this function is designed specifically for this league structure- with no subleagues

@app.route('/lg_history/<league_id>')
def league_history(league_id):
    conn = mysql.connection
    cur = conn.cursor()
    cur.execute(q.get_league_info(league_id))
    info = cur.fetchall()
    cur.execute(q.get_league_history(league_id))
    lg_history = cur.fetchall()
    return render_template('league_history.html', info=info, league_history=lg_history)

#  TODO change free agent row in teams table to blank nickname instead of null
#  TODO turn schools.xml file from game into a db table
#  TODO summary queries to union with player stats queries
#  TODO Current year batting and pitching stats for current roster year
#  TODO in leagues, function to return count of divisions to template that can be used to determine the number of standings and leaders tables to build
#  TODO remove bad stats from league.html template
if __name__ == '__main__':
    app.run()
