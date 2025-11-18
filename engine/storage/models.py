from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import relationship, declarative_base
import datetime

Base = declarative_base()

class PlayerTable(Base):
    __tablename__ = 'players'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    country = Column(String)
    # sourceId = Column(String)

class MatchTable(Base):
    __tablename__ = 'matches'
    id = Column(Integer, primary_key=True)
    venue = Column(String)
    date = Column(DateTime, default=datetime.datetime.utcnow)
    teamA = Column(String)
    teamB = Column(String)
    format = Column(String)



class InningsTable(Base):
    __tablename__ = 'innings'
    id = Column(Integer, primary_key=True)
    match_id = Column(Integer, ForeignKey('matches.id'))
    # team_batting = Column(String)
    # team_bowling = Column(String)


class BatsmanStatsTable(Base):
    __tablename__ = 'batsman_stats'
    id = Column(Integer, primary_key=True)
    player_id = Column(Integer, ForeignKey('players.id'))
    total_runs = Column(Integer, default=0)
    balls_faced = Column(Integer,default=0)
    fours = Column(Integer,default=0)
    sixes = Column(Integer,default=0)
    strike_rate = Column(Float,default=0)
    average = Column(Float,default=0)
    total_dismissals = Column(Integer,default=0)
    innings_played = Column(Integer,default=0)

class BowlerStatsTable(Base):
    __tablename__ = 'bowler_stats'
    id = Column(Integer, primary_key=True)
    player_id = Column(Integer, ForeignKey('players.id'))
    runs_conceded = Column(Integer)
    wickets = Column(Integer)
    balls_bowled = Column(Integer)
    strike_rate = Column(Float)
    average = Column(Float)

class BatsmanVsBowlerStatsTable(Base):
    __tablename__ = 'batsman_vs_bowler'
    id = Column(Integer, primary_key=True)
    batsman_id = Column(Integer, ForeignKey('players.id'))
    bowler_id = Column(Integer, ForeignKey('players.id'))
    runs = Column(Integer)
    balls = Column(Integer)
    fours = Column(Integer)
    sixes = Column(Integer)
    dismissals = Column(Integer)

class FormatTable(Base):
    __tablename__ = 'formats'
    id = Column(Integer, primary_key=True)
    name = Column(String)

class FormatwiseBatsmanStatsTable(Base):
    __tablename__ = 'formatwise_batsman_stats'
    id = Column(Integer, primary_key=True)
    format_id = Column(Integer, ForeignKey('formats.id'))
    batsman_id = Column(Integer, ForeignKey('players.id'))
    runs = Column(Integer)
    balls = Column(Integer)
    matches = Column(Integer)
    innings = Column(Integer)
    fours = Column(Integer)
    sixes = Column(Integer)
    strike_rate = Column(Float)
    average = Column(Float)
    not_out = Column(Integer)
    half_centuries = Column(Integer)
    centuries = Column(Integer)
    ducks = Column(Integer)
    double_centuries = Column(Integer)
    triple_centuries = Column(Integer)
    four_hundreds = Column(Integer)

class OpponentwiseBatsmanStatsTable(Base):
    __tablename__ = 'opponentwise_batsman_stats'
    id = Column(Integer, primary_key=True)
    opponent_id = Column(Integer, ForeignKey('players.id'))
    batsman_id = Column(Integer, ForeignKey('players.id'))
    runs_home = Column(Integer)
    runs_away = Column(Integer)
    runs_neutral = Column(Integer)
    balls_home = Column(Integer)
    balls_away = Column(Integer)
    balls_neutral = Column(Integer)
    matches_home = Column(Integer)
    matches_away = Column(Integer)
    matches_neutral = Column(Integer)
    innings_home = Column(Integer)
    innings_away = Column(Integer)
    innings_neutral = Column(Integer)
    strike_rate_home = Column(Float)
    strike_rate_away = Column(Float)
    strike_rate_neutral = Column(Float)
    average_home = Column(Float)
    average_away = Column(Float)
    average_neutral = Column(Float)
    half_centuries_home = Column(Integer)
    half_centuries_away = Column(Integer)
    half_centuries_neutral = Column(Integer)
    centuries_home = Column(Integer)
    centuries_away = Column(Integer)
    centuries_neutral = Column(Integer)

class OpponentBowlerwiseBatsmanStatsTable(Base):
    __tablename__ = 'opponent_bowlerwise_batsman_stats'
    id = Column(Integer, primary_key=True)
    opponent_id = Column(Integer, ForeignKey('players.id'))
    bowler_id = Column(Integer, ForeignKey('players.id'))
    runs_home = Column(Integer)
    runs_away = Column(Integer)
    runs_neutral = Column(Integer)
    balls_home = Column(Integer)
    balls_away = Column(Integer)
    balls_neutral = Column(Integer)
    innings_home = Column(Integer)
    innings_away = Column(Integer)
    innings_neutral = Column(Integer)
    strike_rate_home = Column(Float)
    strike_rate_away = Column(Float)
    strike_rate_neutral = Column(Float)
    average_home = Column(Float)
    average_away = Column(Float)
    average_neutral = Column(Float)
    fours_home = Column(Integer)
    sixes_home = Column(Integer)
    fours_away = Column(Integer)
    sixes_away = Column(Integer)
    fours_neutral = Column(Integer)
    sixes_neutral = Column(Integer)
    
    
    
    
    
    
    
    
    
    