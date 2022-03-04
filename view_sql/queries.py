#  Queries for view functions

def teams_in_league(lg_id):
    return f"SELECT teams.name, teams.nickname FROM teams WHERE teams.league_id = {lg_id} ORDER BY name DESC;"

def team_roster(team_id):
    return f"""SELECT DISTINCT team_roster.player_id
    , positions.pos_name
    , players.age
    , CONCAT(players.first_name, ' ', players.last_name) as name
    FROM team_roster INNER JOIN players ON team_roster.player_id = players.player_id
    INNER JOIN positions ON players.position = positions.position
    WHERE team_roster.team_id = {team_id} AND team_roster.list_id = 1 AND players.position IN (1,2,3,4,5,6,7,8,9,10)"""

def team_name(team_id):
    return f"""SELECT teams.name, teams.nickname, teams.logo_file_name FROM teams WHERE teams.team_id = {team_id}"""

def player_bio(player_id):
    return f"""SELECT players.first_name, players.last_name , players.nick_name,
    CASE WHEN players.bats = 2 THEN 'L' WHEN players.bats = 1 THEN 'R' ELSE 'S' END AS bats, 
    CASE WHEN players.throws = 2 THEN 'L' ELSE 'R' END AS throws, players.height, players.weight, players.uniform_number,
    players.team_id, players.age, cities.name, states.name, teams.name, teams.nickname, positions.pos_name,
    players.college, players.draft_year, players.draft_round, players.draft_pick,
    players.draft_overall_pick, players.turned_coach, players.hall_of_fame, teams.logo_file_name, players.player_id, t2.draft_team
    , players.position, players.draft_team_id
    FROM players INNER JOIN cities on cities.city_id = players.city_of_birth_id
    INNER JOIN teams ON teams.team_id = players.team_id
    INNER JOIN positions ON players.position = positions.position
    INNER JOIN states ON cities.state_id = states.state_id
    INNER JOIN (
    SELECT teams.team_id, CONCAT(teams.name, ' ', teams.nickname) as draft_team
    FROM teams
    ) as t2 ON players.draft_team_id = t2.team_id
    WHERE players.player_id = {player_id}
    """

#  TODO add union to sum columns in bat_ and pitch_ history
def player_major_bat_history_ovr(player_id):
    return f"""
    SELECT b.year
        , b.stint
        , l.abbr
        , t.abbr
        , b.g
        , b.ab
        , b.PA
        , b.r
        , b.h
        , b.d as 2b
        , b.t as 3b
        , b.hr
        , b.rbi
        , b.sb
        , b.cs
        , b.bb
        , b.k
        , b.ibb
        , b.hp
        , b.sh
        , b.sf
        , b.gdp
        , b.ci
        , ROUND(b.war,1)
        , b.ba as avg
        , b.krate as `k%`
        , b.bbrate as `bb%`
        , b.obp
        , b.OBPplus as `OBP+`
        , b.slg
        , b.ops
        , b.iso
        , b.babip
        , b.woba
        , b.wRAA
        , b.wRC
        , b.wRCplus
        , t.team_id
    FROM CalcBatting b INNER JOIN players p on b.player_id = p.player_id
    INNER JOIN teams t ON b.team_id = t.team_id
    INNER JOIN leagues l on b.league_id = l.league_id
    WHERE b.player_id = {player_id} AND b.level_id = 1
    ORDER BY b.year ASC, b.stint ASC;
    """

def player_major_bat_history_VL(player_id):
    return f"""
    SELECT b.year
        , b.stint
        , l.abbr
        , t.abbr
        , b.g
        , b.ab
        , b.PA
        , b.r
        , b.h
        , b.d as 2b
        , b.t as 3b
        , b.hr
        , b.rbi
        , b.sb
        , b.cs
        , b.bb
        , b.k
        , b.ibb
        , b.hp
        , b.sh
        , b.sf
        , b.gdp
        , b.ci
        , b.war
        , b.ba as avg
        , b.krate as `k%`
        , b.bbrate as `bb%`
        , b.obp
        , b.OBPplus as `OBP+`
        , b.slg
        , b.ops
        , b.iso
        , b.babip
        , b.woba
        , b.wRAA
        , b.wRC
        , b.wRCplus
    FROM CalcBatting_L b INNER JOIN players p on b.player_id = p.player_id
    INNER JOIN teams t ON b.team_id = t.team_id
    INNER JOIN leagues l on b.league_id = l.league_id
    WHERE b.player_id = {player_id} AND b.level_id = 1
    ORDER BY b.year ASC, b.stint ASC;
    """

def player_major_bat_history_VR(player_id):
    return f"""
    SELECT b.year
        , b.stint
        , l.abbr
        , t.abbr
        , b.g
        , b.ab
        , b.PA
        , b.r
        , b.h
        , b.d as 2b
        , b.t as 3b
        , b.hr
        , b.rbi
        , b.sb
        , b.cs
        , b.bb
        , b.k
        , b.ibb
        , b.hp
        , b.sh
        , b.sf
        , b.gdp
        , b.ci
        , b.war
        , b.ba as avg
        , b.krate as `k%`
        , b.bbrate as `bb%`
        , b.obp
        , b.OBPplus as `OBP+`
        , b.slg
        , b.ops
        , b.iso
        , b.babip
        , b.woba
        , b.wRAA
        , b.wRC
        , b.wRCplus
    FROM CalcBatting_R b INNER JOIN players p on b.player_id = p.player_id
    INNER JOIN teams t ON b.team_id = t.team_id
    INNER JOIN leagues l on b.league_id = l.league_id
    WHERE b.player_id = {player_id} AND b.level_id = 1
    ORDER BY b.year ASC, b.stint ASC;
    """

def player_minors_bat_history_ovr(player_id):
    return f"""
    SELECT b.year
        , b.stint
        , l.abbr
        , t.abbr
        , b.g
        , b.ab
        , b.PA
        , b.r
        , b.h
        , b.d as 2b
        , b.t as 3b
        , b.hr
        , b.rbi
        , b.sb
        , b.cs
        , b.bb
        , b.k
        , b.ibb
        , b.hp
        , b.sh
        , b.sf
        , b.gdp
        , b.ci
        , b.war
        , b.ba as avg
        , b.krate as `k%`
        , b.bbrate as `bb%`
        , b.obp
        , b.OBPplus as `OBP+`
        , b.slg
        , b.ops
        , b.iso
        , b.babip
        , b.woba
        , b.wRAA
        , b.wRC
        , b.wRCplus
        , t.team_id
    FROM CalcBatting b INNER JOIN players p on b.player_id = p.player_id
    INNER JOIN teams t ON b.team_id = t.team_id
    INNER JOIN leagues l on b.league_id = l.league_id
    WHERE b.player_id = {player_id} AND b.level_id > 1
    ORDER BY b.year ASC, b.stint ASC;
    """

def player_minors_bat_history_VL(player_id):
    return f"""
    SELECT b.year
        , b.stint
        , l.abbr
        , t.abbr
        , b.g
        , b.ab
        , b.PA
        , b.r
        , b.h
        , b.d as 2b
        , b.t as 3b
        , b.hr
        , b.rbi
        , b.sb
        , b.cs
        , b.bb
        , b.k
        , b.ibb
        , b.hp
        , b.sh
        , b.sf
        , b.gdp
        , b.ci
        , b.war
        , b.ba as avg
        , b.krate as `k%`
        , b.bbrate as `bb%`
        , b.obp
        , b.OBPplus as `OBP+`
        , b.slg
        , b.ops
        , b.iso
        , b.babip
        , b.woba
        , b.wRAA
        , b.wRC
        , b.wRCplus
    FROM CalcBatting_L b INNER JOIN players p on b.player_id = p.player_id
    INNER JOIN teams t ON b.team_id = t.team_id
    INNER JOIN leagues l on b.league_id = l.league_id
    WHERE b.player_id = {player_id} AND b.level_id > 1
    ORDER BY b.year ASC, b.stint ASC;
    """

def player_minors_bat_history_VR(player_id):
    return f"""
    SELECT b.year
        , b.stint
        , l.abbr
        , t.abbr
        , b.g
        , b.ab
        , b.PA
        , b.r
        , b.h
        , b.d as 2b
        , b.t as 3b
        , b.hr
        , b.rbi
        , b.sb
        , b.cs
        , b.bb
        , b.k
        , b.ibb
        , b.hp
        , b.sh
        , b.sf
        , b.gdp
        , b.ci
        , b.war
        , b.ba as avg
        , b.krate as `k%`
        , b.bbrate as `bb%`
        , b.obp
        , b.OBPplus as `OBP+`
        , b.slg
        , b.ops
        , b.iso
        , b.babip
        , b.woba
        , b.wRAA
        , b.wRC
        , b.wRCplus
    FROM CalcBatting_R b INNER JOIN players p on b.player_id = p.player_id
    INNER JOIN teams t ON b.team_id = t.team_id
    INNER JOIN leagues l on b.league_id = l.league_id
    WHERE b.player_id = {player_id} AND b.level_id > 1
    ORDER BY b.year ASC, b.stint ASC;
    """

def player_major_pitch_history_ovr(player_id):
    return f"""
    SELECT p.year
    , p.stint
    , l.abbr
    , t.abbr
    , p.ip
    , p.ab
    , p.tb
    , p.ha
    , p.k
    , p.bf
    , p.rs
    , p.bb
    , p.r
    , p.er
    , p.gb
    , p.fb
    , p.pi
    , p.ipf
    , p.g
    , p.gs
    , p.w
    , p.l
    , p.s
    , p.sa as 1b
    , p.da as 2b
    , p.ta as 3b
    , p.sh
    , p.sf
    , p.hra as hr
    , p.bk
    , p.ci
    , p.iw as ibb
    , p.wp
    , p.hp as hbp
    , p.gf
    , p.dp
    , p.qs
    , p.svo
    , p.bs
    , p.ra
    , p.cg
    , p.sho
    , p.sb
    , p.cs
    , p.hld
    , p.ir
    , p.irs
    , p.wpa
    , p.li
    , p.outs
    , p.war
    , p.InnPitch
    , p.k9
    , p.bb9
    , p.HR9
    , p.WHIP
    , p.`K/BB`
    , p.`gb/fb`
    , p.BABIP
    , p.ERA
    , p.FIP
    , p.xFIP
    , p.ERAminus as `ERA-`
    , p.ERAplus as `ERA+`
    , p.FIPminus as `FIP-`
    , t.team_id

FROM CalcPitching p INNER JOIN teams t on p.team_id = t.team_id
INNER JOIN players ON players.player_id = p.player_id
INNER JOIN leagues l on p.league_id = l.league_id
WHERE p.player_id = {player_id} AND p.level_id = 1
ORDER BY p.year ASC, p.stint ASC;"""

def player_major_pitch_history_VL(player_id):
    return f"""
    SELECT p.year
    , p.stint
    , l.abbr
    , t.abbr
    , p.ip
    , p.ab
    , p.tb
    , p.ha
    , p.k
    , p.bf
    , p.rs
    , p.bb
    , p.r
    , p.er
    , p.gb
    , p.fb
    , p.pi
    , p.ipf
    , p.g
    , p.gs
    , p.w
    , p.l
    , p.s
    , p.sa as 1b
    , p.da as 2b
    , p.ta as 3b
    , p.sh
    , p.sf
    , p.hra as hr
    , p.bk
    , p.ci
    , p.iw as ibb
    , p.wp
    , p.hp as hbp
    , p.gf
    , p.dp
    , p.qs
    , p.svo
    , p.bs
    , p.ra
    , p.cg
    , p.sho
    , p.sb
    , p.cs
    , p.hld
    , p.ir
    , p.irs
    , p.wpa
    , p.li
    , p.outs
    , p.war
    , p.InnPitch
    , p.k9
    , p.bb9
    , p.HR9
    , p.WHIP
    , p.`K/BB`
    , p.`gb/fb`
    , p.BABIP
    , p.ERA
    , p.FIP
    , p.xFIP
    , p.ERAminus as `ERA-`
    , p.ERAplus as `ERA+`
    , p.FIPminus as `FIP-`

FROM CalcPitching_L p INNER JOIN teams t on p.team_id = t.team_id
INNER JOIN players ON players.player_id = p.player_id
INNER JOIN leagues l on p.league_id = l.league_id
WHERE p.player_id = {player_id} AND p.level_id = 1
ORDER BY p.year ASC, p.stint ASC;"""

def player_major_pitch_history_VR(player_id):
    return f"""
    SELECT p.year
    , p.stint
    , l.abbr
    , t.abbr
    , p.ip
    , p.ab
    , p.tb
    , p.ha
    , p.k
    , p.bf
    , p.rs
    , p.bb
    , p.r
    , p.er
    , p.gb
    , p.fb
    , p.pi
    , p.ipf
    , p.g
    , p.gs
    , p.w
    , p.l
    , p.s
    , p.sa as 1b
    , p.da as 2b
    , p.ta as 3b
    , p.sh
    , p.sf
    , p.hra as hr
    , p.bk
    , p.ci
    , p.iw as ibb
    , p.wp
    , p.hp as hbp
    , p.gf
    , p.dp
    , p.qs
    , p.svo
    , p.bs
    , p.ra
    , p.cg
    , p.sho
    , p.sb
    , p.cs
    , p.hld
    , p.ir
    , p.irs
    , p.wpa
    , p.li
    , p.outs
    , p.war
    , p.InnPitch
    , p.k9
    , p.bb9
    , p.HR9
    , p.WHIP
    , p.`K/BB`
    , p.`gb/fb`
    , p.BABIP
    , p.ERA
    , p.FIP
    , p.xFIP
    , p.ERAminus as `ERA-`
    , p.ERAplus as `ERA+`
    , p.FIPminus as `FIP-`

FROM CalcPitching_R p INNER JOIN teams t on p.team_id = t.team_id
INNER JOIN players ON players.player_id = p.player_id
INNER JOIN leagues l on p.league_id = l.league_id
WHERE p.player_id = {player_id} AND p.level_id = 1
ORDER BY p.year ASC, p.stint ASC;"""

def player_minor_pitch_history_ovr(player_id):
    return f"""
    SELECT p.year
    , p.stint
    , l.abbr
    , t.abbr
    , p.ip
    , p.ab
    , p.tb
    , p.ha
    , p.k
    , p.bf
    , p.rs
    , p.bb
    , p.r
    , p.er
    , p.gb
    , p.fb
    , p.pi
    , p.ipf
    , p.g
    , p.gs
    , p.w
    , p.l
    , p.s
    , p.sa as 1b
    , p.da as 2b
    , p.ta as 3b
    , p.sh
    , p.sf
    , p.hra as hr
    , p.bk
    , p.ci
    , p.iw as ibb
    , p.wp
    , p.hp as hbp
    , p.gf
    , p.dp
    , p.qs
    , p.svo
    , p.bs
    , p.ra
    , p.cg
    , p.sho
    , p.sb
    , p.cs
    , p.hld
    , p.ir
    , p.irs
    , p.wpa
    , p.li
    , p.outs
    , p.war
    , p.InnPitch
    , p.k9
    , p.bb9
    , p.HR9
    , p.WHIP
    , p.`K/BB`
    , p.`gb/fb`
    , p.BABIP
    , p.ERA
    , p.FIP
    , p.xFIP
    , p.ERAminus as `ERA-`
    , p.ERAplus as `ERA+`
    , p.FIPminus as `FIP-`
    , t.team_id

FROM CalcPitching p INNER JOIN teams t on p.team_id = t.team_id
INNER JOIN players ON players.player_id = p.player_id
INNER JOIN leagues l on p.league_id = l.league_id
WHERE p.player_id = {player_id} AND p.level_id > 1
ORDER BY p.year ASC, p.stint ASC;"""

def player_minor_pitch_history_VL(player_id):
    return f"""
    SELECT p.year
    , p.stint
    , l.abbr
    , t.abbr
    , p.ip
    , p.ab
    , p.tb
    , p.ha
    , p.k
    , p.bf
    , p.rs
    , p.bb
    , p.r
    , p.er
    , p.gb
    , p.fb
    , p.pi
    , p.ipf
    , p.g
    , p.gs
    , p.w
    , p.l
    , p.s
    , p.sa as 1b
    , p.da as 2b
    , p.ta as 3b
    , p.sh
    , p.sf
    , p.hra as hr
    , p.bk
    , p.ci
    , p.iw as ibb
    , p.wp
    , p.hp as hbp
    , p.gf
    , p.dp
    , p.qs
    , p.svo
    , p.bs
    , p.ra
    , p.cg
    , p.sho
    , p.sb
    , p.cs
    , p.hld
    , p.ir
    , p.irs
    , p.wpa
    , p.li
    , p.outs
    , p.war
    , p.InnPitch
    , p.k9
    , p.bb9
    , p.HR9
    , p.WHIP
    , p.`K/BB`
    , p.`gb/fb`
    , p.BABIP
    , p.ERA
    , p.FIP
    , p.xFIP
    , p.ERAminus as `ERA-`
    , p.ERAplus as `ERA+`
    , p.FIPminus as `FIP-`

FROM CalcPitching_L p INNER JOIN teams t on p.team_id = t.team_id
INNER JOIN players ON players.player_id = p.player_id
INNER JOIN leagues l on p.league_id = l.league_id
WHERE p.player_id = {player_id} AND p.level_id > 1
ORDER BY p.year ASC, p.stint ASC;"""

def player_minor_pitch_history_VR(player_id):
    return f"""
    SELECT p.year
    , p.stint
    , l.abbr
    , t.abbr
    , p.ip
    , p.ab
    , p.tb
    , p.ha
    , p.k
    , p.bf
    , p.rs
    , p.bb
    , p.r
    , p.er
    , p.gb
    , p.fb
    , p.pi
    , p.ipf
    , p.g
    , p.gs
    , p.w
    , p.l
    , p.s
    , p.sa as 1b
    , p.da as 2b
    , p.ta as 3b
    , p.sh
    , p.sf
    , p.hra as hr
    , p.bk
    , p.ci
    , p.iw as ibb
    , p.wp
    , p.hp as hbp
    , p.gf
    , p.dp
    , p.qs
    , p.svo
    , p.bs
    , p.ra
    , p.cg
    , p.sho
    , p.sb
    , p.cs
    , p.hld
    , p.ir
    , p.irs
    , p.wpa
    , p.li
    , p.outs
    , p.war
    , p.InnPitch
    , p.k9
    , p.bb9
    , p.HR9
    , p.WHIP
    , p.`K/BB`
    , p.`gb/fb`
    , p.BABIP
    , p.ERA
    , p.FIP
    , p.xFIP
    , p.ERAminus as `ERA-`
    , p.ERAplus as `ERA+`
    , p.FIPminus as `FIP-`

FROM CalcPitching_R p INNER JOIN teams t on p.team_id = t.team_id
INNER JOIN players ON players.player_id = p.player_id
INNER JOIN leagues l on p.league_id = l.league_id
WHERE p.player_id = {player_id} AND p.level_id > 1
ORDER BY p.year ASC, p.stint ASC;"""

def player_career_bat_summary(player_id):
    return f"""
    SELECT sum(b.g) as g
    , sum(b.ab) as ab
    , sum(b.r) as r
    , sum(b.h) as h
    , sum(b.d) as 2b
    , sum(b.t) as 3b
    , sum(b.hr) as hr
    , sum(b.rbi) as rbi
    , sum(b.sb) as sb
    , sum(b.cs) as cs
    , sum(b.bb) as bb
    , sum(b.k) as k
    , sum(b.ibb) as ibb
    , sum(b.hp) as hp
    , sum(b.sh) as sh
    , sum(b.sf) as sf
    , sum(b.gdp) as gdp
    , sum(b.ci) as ci
    , ROUND(sum(b.war),1) as war
    , ROUND(sum(b.h)/sum(b.ab), 3) as `avg`
    , IF(sum(b.pa) = 0, NULL, ROUND(sum(b.k)/sum(b.pa))) as `k%`
    , IF(sum(b.pa) = 0, NULL, ROUND(sum(b.bb)/sum(b.pa))) as `bb%`
    , ROUND(x.numerator / x.denominator,3) as obp
    , '--' as `obp+`
    , ROUND((sum(b.h)+sum(b.d)+2*sum(b.t)+3*sum(b.hr))/sum(b.ab),3) as slg
    , ROUND((x.numerator/x.denominator) + ((sum(b.h)+sum(b.d)+2*sum(b.t)+3*sum(b.hr))/sum(b.ab)),3) as ops
    , ROUND((sum(b.h)+sum(b.d)+2*sum(b.t)+3*sum(b.hr))/sum(b.ab),3) - ROUND(sum(b.h)/sum(b.ab), 3) as iso
    , IF(sum(b.ab)-sum(b.k)-sum(b.hr)+sum(b.sf)=0,0, round((sum(b.h)-sum(b.hr))/(sum(b.ab)-sum(b.k)-sum(b.hr)+sum(b.sf)),3)) as babip
    , '--'as woba
    , '--' as wraa
    , '--' as wrc
    , '--' as wRCplus
    , COUNT(*) as yrs
    , t.abbr as `team`
    , l.abbr as `lg`
    , l.league_level as lvl
    , sum(b.PA) as pa

FROM CalcBatting b INNER JOIN teams t on b.team_id = t.team_id
INNER JOIN leagues l on b.league_id = l.league_id
INNER JOIN (SELECT b.player_id, t.abbr as team, l.abbr as lg, l.league_level, sum(b.h) + sum(b.bb) + sum(b.hp)  as numerator
            , sum(b.pa) - sum(b.sh) - sum(b.ci) as denominator
            FROM CalcBatting b
            INNER JOIN teams t on b.team_id = t.team_id
            INNER JOIN leagues l on b.league_id = l.league_id
            GROUP BY b.player_id, team, lg, l.league_level
) as x ON b.player_id = x.player_id AND t.abbr = x.team AND l.abbr = x.lg AND l.league_level = x.league_level
WHERE b.player_id = {player_id}
GROUP BY t.abbr, '--', '--', '--', '--', '--', ROUND(x.numerator / x.denominator,3), l.abbr, l.league_level
    """

def player_career_pitch_summary(player_id):
    return f"""
    SELECT ROUND(sum(p.outs)/3,1) as ip
    , sum(p.ab) as ab
    , sum(p.tb) as tb
    , sum(p.ha) as ha
    , sum(p.k) as k
    , sum(p.bf) as bf
    , sum(p.rs) as rs
    , sum(p.bb) as bb
    , sum(p.r) as r
    , sum(p.er) as er
    , sum(p.gb) as gb
    , sum(p.fb) as fb
    , sum(p.pi) as pi
    , sum(p.g) as g
    , sum(p.gs) as gs
    , sum(p.w) as w
    , sum(p.l) as l
    , sum(p.s) as s
    , sum(p.sa) as 1B
    , sum(p.da) as 2B
    , sum(p.ta) as 3B
    , sum(p.hra) as HR
    , sum(p.sh) as sh
    , sum(p.sf) as sf
    , sum(p.bk) as bk
    , sum(p.ci) as ci
    , sum(p.iw) as ibb
    , sum(p.wp) as wp
    , sum(p.hp) as hbp
    , sum(p.gf) as gf
    , sum(p.dp) as dp
    , sum(p.qs) as qs
    , sum(p.svo) as svo
    , sum(p.bs) as bs
    , sum(p.ra) as ra
    , sum(p.cg) as cg
    , sum(p.sho) as sho
    , sum(p.sb) as sb
    , sum(p.cs) as cs
    , sum(p.hld) as hld
    , sum(p.ir) as ir
    , sum(p.irs) as irs
    , sum(p.wpa) as wpa
    , sum(p.li) as li
    , sum(p.outs) as outs
    , ROUND(sum(war),1) as war
    , ROUND(sum(p.k)/(sum(p.InnPitch)/9),1) as k9
    , ROUND(sum(p.bb)/(sum(InnPitch)/9),1) as bb9
    , ROUND(sum(p.hra)/(sum(InnPitch)/9),1) as hr9
    , ROUND((sum(p.bb) + sum(p.ha))/sum(p.InnPitch),2) as WHIP
    , ROUND(sum(p.k)/sum(p.bb),2) as `k/bb`
    , ROUND(sum(p.gb)/sum(p.fb),2) as `gb/fb`
    , t.abbr as team
    , l.abbr as lg
    , l.league_level
    , COUNT(*) as yrs

FROM CalcPitching p INNER JOIN teams t on p.team_id = t.team_id
INNER JOIN leagues l on p.league_id=l.league_id
WHERE p.player_id={player_id}
GROUP BY t.abbr, l.abbr, l.league_level
    """

def team_history_record(team_id):
    return f"""
    SELECT thr.year
    , thr.g
    , thr.w
    , thr.l
    , thr.pos
    , ROUND(thr.pct, 3) AS pct
    , thr.gb
    , CONCAT(p1.first_name, ' ', p1.last_name) as hitter
    , CONCAT(p2.first_name, ' ', p2.last_name) as pitcher
    , CONCAT(p3.first_name, ' ', p3.last_name) as rookie
    , CONCAT(c.first_name, ' ', c.last_name) as manager
    , CASE
        WHEN th.made_playoffs = 0 THEN ''
        WHEN th.made_playoffs = 1 THEN 'Made Playoffs'
        END AS Playoffs
    , CASE
        WHEN th.won_playoffs = 0 THEN ''
        WHEN th.made_playoffs = 1 THEN 'Won Playoffs'
        END AS Won_Playoffs
    , th.best_hitter_id
    , th.best_pitcher_id
    , th.best_rookie_id
    , th.manager_id

FROM team_history_record thr
INNER JOIN team_history th ON thr.team_id=th.team_id AND thr.year=th.year
INNER JOIN players p1 ON th.best_hitter_id = p1.player_id
INNER JOIN players p2 ON th.best_pitcher_id = p2.player_id
INNER JOIN players p3 ON th.best_rookie_id = p3.player_id
INNER JOIN coaches c ON th.manager_id = c.coach_id
WHERE thr.team_id = {team_id}
ORDER BY thr.year asc
"""

def team_current_staff(team_id):
    return f"""
    SELECT CONCAT(c1.first_name, ' ', c1.last_name) as scout_name
    , trs.head_scout
    , c1.former_player_id as scout_frmr_pl_id
    , CONCAT(c2.first_name, ' ', c2.last_name) as manager_name
    , trs.manager
    , c2.former_player_id as mgr_frmr_pl_id
    , CONCAT(c3.first_name, ' ', c3.last_name) as gm_name
    , trs.general_manager
    , c3.former_player_id as gm_frmr_pl_id
    , CONCAT(c4.first_name, ' ', c4.last_name) as pc_name
    , trs.pitching_coach
    , c4.former_player_id as pc_frmr_pl_id
    , CONCAT(c5.first_name, ' ', c5.last_name) as hc_name
    , trs.hitting_coach
    , c5.former_player_id as hc_frmr_pl_id
    , CONCAT(c6.first_name, ' ', c6.last_name) as bc_name
    , trs.bench_coach
    , c6.former_player_id as bc_frmr_pl_id
    , CONCAT(c7.first_name, ' ', c7.last_name) as owner_name
    , trs.owner
    , c7.former_player_id as own_frmr_pl_id
    , CONCAT(c8.first_name, ' ', c8.last_name) as dr_name
    , trs.doctor
    , c8.former_player_id as dr_frmr_pl_id
    , CONCAT(c9.first_name, ' ', c9.last_name) as 1b_name
    , trs.first_base_coach
    , c9.former_player_id as 1b_frmr_pl_id
    , CONCAT(c10.first_name, ' ', c10.last_name) as 3b_name
    , trs.third_base_coach
    , c10.former_player_id as 3b_frmr_pl_id

FROM team_roster_staff trs INNER JOIN coaches c1 ON trs.head_scout=c1.coach_id
INNER JOIN coaches c2 ON trs.manager = c2.coach_id
INNER JOIN coaches c3 ON trs.general_manager = c3.coach_id
INNER JOIN coaches c4 ON trs.pitching_coach = c4.coach_id
INNER JOIN coaches c5 ON trs.hitting_coach = c5.coach_id
INNER JOIN coaches c6 ON trs.bench_coach = c6.coach_id
INNER JOIN coaches c7 ON trs.owner = c7.coach_id
INNER JOIN coaches c8 ON trs.doctor = c8.coach_id
INNER JOIN coaches c9 ON trs.first_base_coach = c9.coach_id
INNER JOIN coaches c10 ON trs.third_base_coach = c10.coach_id
WHERE trs.team_id = {team_id}
"""

def team_affiliates(team_id):
    return f"""
    SELECT t1.name
    , t1.abbr
    , t1.nickname
    , t1.logo_file_name
    , l.name as league_name
    , l.abbr as lg_abbr
    , t1.team_id
    , l.league_level
FROM teams t1
INNER JOIN leagues l ON t1.league_id=l.league_id AND t1.level = l.league_level
WHERE t1.parent_team_id = {team_id}
ORDER BY l.league_level ASC
    """

#  Functions to create team_year page
def list_of_starters(starters):
    try:
        delist = [starter[0] for starter in starters]
        starter_ids_list = [item[0] for item in delist]
        strings = ''
        for item in starter_ids_list:
            strings += str(item) + ","
        strings = strings[:-1]
        starter_ids = "(" + strings + ")"
        return starter_ids
    except IndexError:
        starter_ids = '()'
        return starter_ids


#  The max_gs function below is broken.  Not in use.
def max_gs(team_id, year):
    cur.execute(f"""
    SELECT pi.player_id, pi.gs
    FROM rb1.CalcPitching pi
    WHERE pi.team_id = {team_id} AND pi.year = {year}
    ORDER BY pi.gs DESC 
    LIMIT 5""")
    result = cur.fetchall()
    starter_ids = q.list_of_starters(result)
    return starter_ids

def team_year_batters_starters(team_id, year, starter_ids):
    return f"""
SELECT p.player_id
   , CONCAT(p.first_name, ' ', p.last_name) as player
   , b.g
   , pos.pos_name as position
   , p.position
   , b.year
   , b.team_id
   , CONCAT(t.name, ' ', t.nickname) AS team_name
   , b.ab
   , b.h
   , b.k
   , b.bb
   , b.ba
   , b.slg
   , b.obp
   , b.woba
   , ROUND(b.war,1) as war
   , b.r

FROM CalcBatting b INNER JOIN players p on b.player_id = p.player_id
INNER JOIN positions pos on p.position = pos.position
INNER JOIN teams t ON b.team_id=t.team_id
WHERE b.team_id = {team_id} AND b.year = {year} AND b.player_id IN {starter_ids}
ORDER BY p.position asc
"""

def team_year_batters_bench(team_id, year, starter_ids):
    return f"""
SELECT p.player_id
   , CONCAT(p.first_name, ' ', p.last_name) as player
   , b.g
   , pos.pos_name as position
   , p.position
   , b.year
   , b.team_id
   , CONCAT(t.name, ' ', t.nickname) AS team_name
   , b.ab
   , b.h
   , b.k
   , b.bb
   , b.ba
   , b.slg
   , b.obp
   , b.woba
   , ROUND(b.war,1) as war

FROM CalcBatting b INNER JOIN players p on b.player_id = p.player_id
INNER JOIN positions pos on p.position = pos.position
INNER JOIN teams t ON b.team_id=t.team_id
WHERE b.team_id = {team_id} AND b.year = {year} AND b.player_id NOT IN {starter_ids}
ORDER BY p.position asc
"""

def team_year_all_batters(team_id, year):
    return f"""
SELECT p.player_id
   , CONCAT(p.first_name, ' ', p.last_name) as player
   , b.g
   , pos.pos_name as position
   , p.position
   , b.year
   , b.team_id
   , CONCAT(t.name, ' ', t.nickname) AS team_name
   , b.ab
   , b.h
   , b.k
   , b.bb
   , b.ba
   , b.slg
   , b.obp
   , b.woba
   , ROUND(b.war,1) as war

FROM CalcBatting b INNER JOIN players p on b.player_id = p.player_id
INNER JOIN positions pos on p.position = pos.position
INNER JOIN teams t ON b.team_id=t.team_id
WHERE b.team_id = {team_id} AND b.year = {year}
ORDER BY p.position asc
"""

def team_year_starting_p(team_id, year):
    return f"""
    SELECT p.player_id
        , CONCAT(pl.first_name, ' ', pl.last_name) as name
        , p.w
        , p.l
        , p.ERA
        , p.g
        , p.gs
        , p.cg
        , p.sho
        , p.s
        , ROUND(p.InnPitch,1) as IP
        , p.ha as h
        , p.r
        , p.er
        , p.hra
        , p.bb
        , p.iw as ibb
        , p.k
        , p.hp
        , p.bk
        , p.wp
        , p.bf
        , p.ERAplus
        , p.FIP
        , p.WHIP
        , p.k9
        , p.bb9
        , p.`K/BB`
        , ROUND(p.war,1) as war
        
    FROM CalcPitching p INNER JOIN players pl ON p.player_id = pl.player_id
    WHERE p.team_id = {team_id} AND p.year = {year} AND pl.position = 1 AND pl.role = 11
    ORDER BY p.gs DESC
    """

def team_year_bullpen_p(team_id, year):
    return f"""
    SELECT p.player_id
        , CONCAT(pl.first_name, ' ', pl.last_name) as name
        , p.w
        , p.l
        , p.ERA
        , p.g
        , p.gs
        , p.cg
        , p.sho
        , p.s
        , ROUND(p.InnPitch,1) as IP
        , p.ha as h
        , p.r
        , p.er
        , p.hra
        , p.bb
        , p.iw as ibb
        , p.k
        , p.hp
        , p.bk
        , p.wp
        , p.bf
        , p.ERAplus
        , p.FIP
        , p.WHIP
        , p.k9
        , p.bb9
        , p.`K/BB`
        , ROUND(p.war,1) as war

    FROM CalcPitching p INNER JOIN players pl ON p.player_id = pl.player_id
 WHERE p.team_id = {team_id} AND p.year = {year} AND pl.position = 1 AND pl.role <> 11
    ORDER BY p.g DESC
    """

def team_year_best_players(team_id, year):
    return f"""
    SELECT x.name, x.war, x.player_id
FROM
(SELECT CONCAT(p.first_name, ' ', p.last_name) as name
    , ROUND(b.war,1) as war
    , b.player_id
FROM players p INNER JOIN CalcBatting b ON p.player_id = b.player_id
WHERE b.team_id = {team_id} AND b.year = {year}
UNION
SELECT CONCAT(p1.first_name, ' ', p1.last_name) as name
    , ROUND(p.war,1) as war
    , p.player_id
FROM players p1 INNER JOIN CalcPitching p ON p1.player_id = p.player_id
WHERE p.team_id = {team_id} AND p.year = {year}) as x
ORDER BY war desc
LIMIT 10
    """

def team_year_record(team_id, year):
    return f"""
    SELECT team_id, year, w, l, pos, round(pct,3) as pct, gb, leagues.name, divisions.name, sub_leagues.name    
    FROM team_history_record INNER JOIN leagues ON team_history_record.league_id = leagues.league_id 
    INNER JOIN divisions ON team_history_record.division_id = divisions.division_id AND divisions.league_id = leagues.league_id
    INNER JOIN rb1.sub_leagues ON team_history_record.sub_league_id = sub_leagues.sub_league_id and sub_leagues.league_id = leagues.league_id
    WHERE team_id = {team_id} AND year = {year}"""

def current_world_date():
    return f"""
    SELECT MAX(leagues.current_date) as current_world_date
    FROM leagues"""

# Get a list of major leagues
def get_major_leagues():
    return "SELECT leagues.league_id FROM leagues WHERE league_level =1"

def get_affiliated_leagues():
    return f"""
    SELECT league_id
    , abbr
    , name
    , logo_file_name
    , league_level
    , parent_league_id
    FROM leagues
    """

def get_div_records(league_id, division_id, sub_league_id=0):
    return f"""
    SELECT t.division_id
    , tr.team_id
    , tr.g
    , tr.w
    , tr.l
    , tr.pos
    , tr.pct
    , tr.gb
    , tr.streak
    , tr.magic_number
    , t.abbr
    , t.name
    , t.nickname
    , t.logo_file_name
    , t.league_id
    , l.name
    , l.parent_league_id
    , d.name

FROM team_record tr INNER JOIN teams t ON tr.team_id = t.team_id
INNER JOIN divisions d ON t.division_id = d.division_id AND t.league_id=d.league_id
INNER JOIN leagues l ON l.league_id = t.league_id AND l.league_id=d.league_id
WHERE t.league_id = {league_id} AND t.division_id = {division_id}
ORDER BY tr.gb ASC
    """

def get_top_5_leaders_historical(league_id, year, division_id):
    return f"""
    SELECT CONCAT(p.first_name, ' ', p.last_name) as player
, pll.category
, m.stat_short
, m.stat_long
, pll.place
, pll.amount
, pll.league_id
, pll.year
, t.abbr
, t.division_id
, pll.player_id


FROM players_league_leader pll INNER JOIN players p on pll.player_id=p.player_id
INNER JOIN players_league_leader_map m ON pll.category=m.category
INNER JOIN teams t ON p.team_id=t.team_id
WHERE pll.category IN (2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,18,19,20,22,23,25,26,27,28,30,31,32,34,36,38,40,41,42,43,46,47,48,49,54,56,58,59)
AND pll.league_id = {league_id} AND pll.year = {year} AND t.division_id = {division_id} AND pll.place <=5
ORDER BY pll.category asc, pll.place asc
    """

def get_divs_from_league(league_id):
    return f"""
    SELECT division_id, name FROM rb1.divisions WHERE league_id={league_id}"""

def get_current_league_bat_leaders(league_id, division_id, year, stat):
    """Used to get current year batting leaders """
    return f"""
    SELECT CONCAT(p.first_name, ' ', p.last_name) as name
, b.player_id
, b.team_id
, d.division_id
, d.name as div_name
, t.abbr
, b.{stat}
, b.year
, b.league_id
FROM CalcBatting b INNER JOIN players p ON b.player_id=p.player_id
INNER JOIN teams t ON t.team_id = b.team_id AND p.team_id=b.team_id AND t.team_id=p.team_id
INNER JOIN divisions d ON t.division_id=d.division_id AND d.league_id = b.league_id AND d.league_id=t.league_id
WHERE b.league_id={league_id} AND b.year={year} AND d.division_id={division_id}
ORDER BY b.{stat} DESC
LIMIT 5
    """

def get_batting_stats_from_map():
    return f"""
    SELECT category, stat_short, calc_name
    FROM players_league_leader_map
    WHERE b_p = 'B'
    """

def get_current_pitch_stats_asc_from_map():
    return """
    SELECT category, stat_short, calc_name
    FROM players_league_leader_map
    WHERE category IN (40,41,42,46,47)
    """

def get_current_pitch_stats_desc_from_map():
    return """
    SELECT category, stat_short, calc_name
    FROM players_league_leader_map
    WHERE category NOT IN (40,41,42,46,47) AND b_p = 'P'
    """

def get_current_pitch_leaders_asc(league_id, division_id, year, stat):
    return f"""
SELECT CONCAT(p.first_name, ' ', p.last_name) as name
, b.player_id
, b.team_id
, d.division_id
, d.name as div_name
, t.abbr
, b.{stat}
, b.year
, b.league_id
FROM rb1.CalcPitching b INNER JOIN players p ON b.player_id=p.player_id
INNER JOIN teams t ON t.team_id = b.team_id AND p.team_id=b.team_id AND t.team_id=p.team_id
INNER JOIN divisions d ON t.division_id=d.division_id AND d.league_id = b.league_id AND d.league_id=t.league_id
WHERE b.league_id={league_id} AND b.year={year} AND d.division_id={division_id}
ORDER BY b.{stat} ASC
LIMIT 5
    """

def get_current_pitch_leaders_desc(league_id, division_id, year, stat):
    return f"""
SELECT CONCAT(p.first_name, ' ', p.last_name) as name
, b.player_id
, b.team_id
, d.division_id
, d.name as div_name
, t.abbr
, b.{stat}
, b.year
, b.league_id
FROM rb1.CalcPitching b INNER JOIN players p ON b.player_id=p.player_id
INNER JOIN teams t ON t.team_id = b.team_id AND p.team_id=b.team_id AND t.team_id=p.team_id
INNER JOIN divisions d ON t.division_id=d.division_id AND d.league_id = b.league_id AND d.league_id=t.league_id
WHERE b.league_id={league_id} AND b.year={year} AND d.division_id={division_id}
ORDER BY b.{stat} desc
LIMIT 5
    """

def get_league_info(league_id):
    return f"""
    SELECT name, abbr, logo_file_name
    FROM leagues
    WHERE league_id={league_id}
    """

def get_league_history(league_id):
    return f"""   
   SELECT th.year
, th.league_id
, th.team_id
, t.name
, t.nickname
, lh.best_hitter_id
, CONCAT(p1.first_name, ' ', p1.last_name) as hitter
, lh.best_pitcher_id
, CONCAT(p2.first_name, ' ', p2.last_name) as pitcher
, lh.best_rookie_id
, CONCAT(p3.first_name, ' ', p3.last_name) as rookie
FROM team_history th INNER JOIN teams t ON th.team_id = t.team_id
INNER JOIN league_history lh ON lh.year = th.year AND lh.league_id = t.league_id
INNER JOIN players p1 ON lh.best_hitter_id = p1.player_id
INNER JOIN players p2 ON lh.best_pitcher_id = p2.player_id
LEFT JOIN players p3 ON lh.best_rookie_id = p3.player_id
WHERE th.won_playoffs = 1 AND th.league_id = {league_id}
ORDER BY th.year"""