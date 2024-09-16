import json
import os
import pandas as pd
import numpy as np
from sshtunnel import SSHTunnelForwarder
from sqlalchemy import create_engine
from sqlalchemy import inspect
from sqlalchemy import text
from sqlalchemy_utils import database_exists, create_database
from sqlalchemy.ext.declarative import declarative_base
import pandas as pd
import os
import json
from scipy.optimize import curve_fit, linprog
from statsmodels import robust
from statsmodels.robust.scale import huber
import matplotlib.pyplot as plt
import seaborn as sns


# import getpass


class DB_connect(object):
    """
    The class 'LT_connect' can be used to connect to the LT postgres database
    via a ssh connection.\n

    Functions:
    ----------

    tables(self, db, schema, sql_user, sql_pass)\n
    print_columns(self, db, table_name, sql_user, sql_pass)\n
    query(self, db, query, sql_user, sql_pass)\n
    execute(self, db, query, sql_user, sql_pass)\n
    insert(self, db, query, data, sql_user, sql_pass)\n
    ret_con(self, db, sql_user, sql_pass)\n
    create_db(self, db, sql_user, sql_pass)

    Parameters
    ----------

    db : name of a postgres database that should be accessed \n
    p_host : address of the database of the system
    (usually localhost - 127.0.0.1) \n
    p_port : port for postgresql (usually 5432) \n
    ssh : if a ssh connection is necessary insert 'True' \n
    ssh_user : account name of the ssh user \n
    ssh_host : ip address of the server to which to connect \n
    ssh_pkey : filepath to the ssh key for faster access \n
    sql_user : account name of the postgres user \n
    sql_pass : password for the postgres account \n

    Return
    ------

    None


    """

    def __init__(
        self,
        ssh,
        ssh_host,
        ssh_port,
        ssh_user,
        keybased,
        ssh_pwd,
        ssh_pkey,
        db_host,
        db_port,
        db,
        sql_user,
        sql_pass,
        dbtype,
        sqlitepath,
    ):
        """
        __init__(self, db_host, db_port, db, ssh, ssh_user, ssh_host, ssh_pkey, sql_user, sql_pass):
        -----------------------------------------------
        defines global class parameters for ssh connection\n

        Parameters
        ----------
        ssh : if a ssh connection is necessary insert 'True' \n
        ssh_host : ip address of the server to which to connect \n
        ssh_port : port of the server to which to connect \n
        ssh_user : account name of the ssh user \n
        keybased : boolean - True if ssh-key is used to connect to server \n
        ssh_pwd : password for ssh connection \n
        ssh_pkey : filepath to the ssh key for faster access \n
        db_host : address of the database of the system
        (usually localhost - 127.0.0.1) \n
        db_port : port for postgresql (usually 5432) \n
        db : name of a postgres database that should be accessed \n
        sql_user : account name of the postgres user \n
        sql_pass : password for the postgres account \n
        dbtype : dbtype used (postgres, mysql, sqlite)

        Returns:
        --------
        None
        """
        # SSH Tunnel Variables
        self.db_host = db_host
        self.db_port = db_port
        self.sql_user = sql_user
        self.sql_pass = sql_pass
        self.ssh_port = ssh_port
        self.dbtype = dbtype
        self.db = db
        self.echoparam = False

        if ssh == True:
            if keybased == True:
                self.server = SSHTunnelForwarder(
                    (ssh_host, ssh_port),
                    ssh_username=ssh_user,
                    ssh_pkey=ssh_pkey,
                    remote_bind_address=(db_host, db_port),
                )
                server = self.server
                server.start()  # start ssh server
                self.local_port = server.local_bind_port
                print(f"Server connected via SSH ...")
            else:
                self.server = SSHTunnelForwarder(
                    (ssh_host, ssh_port),
                    ssh_username=ssh_user,
                    ssh_password=ssh_pwd,
                    remote_bind_address=(db_host, db_port),
                )
                server = self.server
                server.start()  # start ssh server
                self.local_port = server.local_bind_port
                print(f"Server connected via SSH ...")
        else:
            self.local_port = db_port

        if dbtype == "postgres":
            self.enginestr = f"postgresql://{self.sql_user}:{self.sql_pass}@{self.db_host}:{self.local_port}/{self.db}"

        elif dbtype == "mysql":
            self.enginestr = f"mysql+mysqldb://{self.sql_user}:{self.sql_pass}@{self.db_host}:{self.local_port}/{self.db}"

        elif dbtype == "sqlite":
            if not os.path.exists(sqlitepath):
                os.makedirs(sqlitepath)
            self.enginestr = f"sqlite:///{sqlitepath}\\{self.db}.db"

    def tables(self, schema):
        """
        tables(self, db, schema, sql_user, sql_pass):
        -----------------------------------------------
        returns all table names in a given 'schema' of a database 'db'\n

        Parameters:
        ----------

        db : name of a postgres database that should be accessed \n
        schema : name of the schema that should be analyzed\n
        sql_user : account name of the postgres user \n
        sql_pass : password for the postgres account \n

        Returns:
        --------
        tables_df (pandas dataframe of table names)

        """

        # create an engine to connect to the postgreSQL database, documentation
        # of functions can be found at https://docs.sqlalchemy.org/en/14/

        if self.dbtype == "sqlite":
            engine = create_engine(self.enginestr, echo=True)
        else:
            engine = create_engine(self.enginestr)
        conn = engine.connect()
        inspector = inspect(engine)
        tables = inspector.get_table_names(schema=schema)
        self.tables_df = pd.DataFrame(tables, columns=["table name"])
        engine.dispose()
        return self.tables_df

    def print_columns(self, table_name):
        """
        print_columns(self, db, table_name, sql_user, sql_pass)
        -----------------------------------------------
        returns all table names in a given 'schema' of a database 'db'\n

        Parameters:
        ----------

        db : name of a postgres database that should be accessed \n
        table_name : name of the table for which the columns schould be checked \n
        sql_user : account name of the postgres user \n
        sql_pass : password for the postgres account \n

        Returns:
        --------
        tables_df (pandas dataframe of column names)

        """

        # create an engine to connect to the postgreSQL database, documentation
        # of functions can be found at https://docs.sqlalchemy.org/en/14/

        engine = create_engine(self.enginestr, echo=self.echoparam)

        if " " in table_name:
            if '"' in table_name:
                pass
            else:
                table_name = "'" + table_name + "'"
        query = (
            """
        SELECT column_name, data_type
        FROM information_schema.columns
        WHERE table_name = %s
        ;
        """
            % table_name
        )
        self.table_df = pd.read_sql(query, engine)
        engine.dispose()
        return self.table_df

    def query(self, query):
        """
        query(self, db, query, sql_user, sql_pass)
        -----------------------------------------------
        executes a postgreSQL query in the database 'db' (return = true)\n

        Parameters:
        ----------

        db : name of a postgres database that should be accessed \n
        query : insert char string of postgreSQL code that should be queried \n
        sql_user : account name of the postgres user \n
        sql_pass : password for the postgres account \n

        Returns:
        --------
        query_df (pandas dataframe of query result)

        """
        # create an engine to connect to the postgreSQL database, documentation
        # of functions can be found at https://docs.sqlalchemy.org/en/14/
        engine = create_engine(self.enginestr, echo=self.echoparam)
        self.query_df = pd.read_sql(query, engine)
        engine.dispose()
        return self.query_df

    def execute(self, query):
        """
        execute(self, db, query, sql_user, sql_pass)
        -----------------------------------------------
        executes a postgreSQL query in the database 'db' (return = false)\n

        Parameters:
        ----------

        db : name of a postgres database that should be accessed \n
        query : insert char string of postgreSQL code that should be queried \n
        sql_user : account name of the postgres user \n
        sql_pass : password for the postgres account \n

        Returns:
        --------
        None

        """
        # create an engine to connect to the postgreSQL database, documentation
        # of functions can be found at https://docs.sqlalchemy.org/en/14/
        engine = create_engine(self.enginestr, echo=self.echoparam)
        with engine.begin() as connection:
            connection.execute(text(query))
        # engine.execute(text(query))
        engine.dispose()

    def insert(self, query, data):
        """
        insert(self, db, query, data, sql_user, sql_pass)
        -----------------------------------------------
        executes a postgreSQL query in the database 'db' (return = false),
        used to insert data with parameter data, use '%(name)s' in the query text
        and a dictionary ({name : value}) for data \n

        Parameters:
        ----------

        db : name of a postgres database that should be accessed \n
        query : insert char string of postgreSQL code that should be queried \n
        data : dictionary of data that should be used in the query \n
        sql_user : account name of the postgres user \n
        sql_pass : password for the postgres account \n

        Returns:
        --------
        None

        """
        # create an engine to connect to the postgreSQL database, documentation
        # of functions can be found at https://docs.sqlalchemy.org/en/14/
        engine = create_engine(self.enginestr, echo=self.echoparam)

        with engine.begin() as connection:
            connection.execute(text(query), data)
        # engine.execute(text(query), data[0])
        engine.dispose()

    def ret_con(self):
        """
        ret_con(self, db, sql_user, sql_pass)
        -----------------------------------------------
        returns the engine to connect to the database 'db'\n

        Parameters:
        ----------

        db : name of a postgres database that should be accessed \n
        sql_user : account name of the postgres user \n
        sql_pass : password for the postgres account \n

        Returns:
        --------
        engine

        """
        # create an engine to connect to the postgreSQL database, documentation
        # of functions can be found at https://docs.sqlalchemy.org/en/14/
        engine = create_engine(self.enginestr, echo=self.echoparam)
        return engine

    def create_db(self):
        """
        create_db(self, db, sql_user, sql_pass)
        -----------------------------------------------
        creates the database 'db'\n

        Parameters:
        ----------

        db : name of a postgres database that should be accessed \n
        sql_user : account name of the postgres user \n
        sql_pass : password for the postgres account \n

        Returns:
        --------
        None

        """
        # create an engine to connect to the postgreSQL database, documentation
        # of functions can be found at https://docs.sqlalchemy.org/en/14/

        print(self.dbtype)
        if self.dbtype == "sqlite":
            engine = create_engine(self.enginestr, echo=self.echoparam)
            Base = declarative_base()
            Base.metadata.create_all(engine)
        else:
            engine = create_engine(self.enginestr)
            if not database_exists(engine.url):
                create_database(engine.url)
            else:
                print('A database with the name "' + self.db + '" already exists')


def connCowBaseDB(rootdir):
    """
    Returns connection to database, specify parameters in settings file

    Parameters
    ----------
    rootdir : str
        path to cowbase rootdir
    """

    settingsPath = os.path.join(rootdir, "config", "serverSettings.json")

    with open(settingsPath) as file:
        serverSettings = json.load(file)

    # Create a connection to the database
    db_connect = DB_connect(**serverSettings)

    return db_connect


def dailyMY(df_milking):
    """
    Converts raw SESSION milk yield data to standardized DAILY milk yield data
    + some data selection steps (outliers deleted)

    Parameters
    ----------
    df_milking : df
        raw data of one farm from the database containing variables
            * milking_id
            * farm_id
            * animal_id
            * lactation_id
            * parity
            * started_at
            * ended_at
            * mi
            * dim
            * tmy & qmy (mylf, myrf, mylr, myrr)
            * quarter ec (eclf, ecrf, eclr, ecrr)

    Yields
    ------
    df_milking_daily : df
        (daily milk yield) data of one farm containing variables
            * farm_id
            * animal_id
            * lactation_id
            * dim
            * tdmy
            * dmylf, dmyrf, dmylr, dmyrr

    Steps
    -----
        - calculate the proportion of the MI before and after midnight
        - assign that proportion of the MY to the current or previous day (at udder and quarter level)
        - sum the milk yields of each day
        - add 1 to the DIM to avoid problems with log later on
        - standardize by dividing by the sum of all MI assigned to the current day (to account for missing milkings)
        - calculate a 7 day rolling median of the TDMY: delete tdmy values that are lower than 1.5*the rolling median
        - delete observations with TDMY below 75 kg

    """

    # Kick out all entries where mi could not be calculated/was not recorded.
    # This might lead to loss of information, creating a
    # total daily milk yield though would have large deviations if the mi was not guessed correctly.
    df_milking = df_milking.sort_values(
        by=["farm_id", "animal_id", "lactation_id", "milking_id"]
    ).reset_index(drop=True)
    milking = df_milking[df_milking["mi"].notna()].copy()

    # Floor dim for the calculation of daily milk yield
    milking["dim_floor"] = milking["dim"].apply(np.floor)

    # IV_dim_floor gives the time in hours at which the milking started at
    milking["IV_dim_floor"] = 24 * (milking["dim"] - milking["dim_floor"])

    # calculate the time between milkings that was during the previous day (compared to the dim floored)
    milking["mi_day_before"] = milking["mi"] - milking["IV_dim_floor"]
    # you put it to 0 because there was a previous milking on the same day
    milking.loc[milking["mi_day_before"] < 0, "mi_day_before"] = 0

    # calculate the time between milkings that was during the day (dim floored)
    milking["mi_on_day"] = milking["mi"] - milking["mi_day_before"]

    # calulate the proportions of mi on the day and day before
    milking["mi_day_before"] = milking["mi_day_before"] / milking["mi"]
    milking["mi_on_day"] = milking["mi_on_day"] / milking["mi"]

    # create a new table where the time between milkings was spread over two days
    MY_daily_add = milking[milking["mi_day_before"] > 0].copy()

    # multiply the tmy in the first dataset (MY) with the mi in the day to get the propotion of milk yield 'produced' on that day
    # all parts of the milking session before midnight are set to 0. The only milk yields in THIS dataset, are from the sessions completely produced in the current day AND the proportion produced after midnight.
    milking["mi_day_before"] = 0
    milking["tmy"] = milking["tmy"] * milking["mi_on_day"]
    milking["mylf"] = milking["mylf"] * milking["mi_on_day"]
    milking["myrf"] = milking["myrf"] * milking["mi_on_day"]
    milking["mylr"] = milking["mylr"] * milking["mi_on_day"]
    milking["myrr"] = milking["myrr"] * milking["mi_on_day"]

    # multiply the tmy in the second dataset (df_milking_add) with the mi on the day before to get the propotion of milk yield 'produced' on the previous day
    # all complete milk sessions and the part of the milking interval after midnight, are equaled to 0. The only milk yields in THIS dataset are milk yields from the proportion before midnight.
    MY_daily_add["mi_on_day"] = 0
    # change the DIM to the DIM of the previous day (so later you will add this MY to the corresponding day - before midnight)
    MY_daily_add["dim_floor"] -= 1
    # if proportion of MI on the previous day is lower than 0, set equal to 0 (no milk yield assigned to the previous day)
    MY_daily_add[MY_daily_add["dim_floor"] < 0] = 0
    MY_daily_add["tmy"] = MY_daily_add["tmy"] * MY_daily_add["mi_day_before"]
    MY_daily_add["mylf"] = MY_daily_add["mylf"] * MY_daily_add["mi_day_before"]
    MY_daily_add["myrf"] = MY_daily_add["myrf"] * MY_daily_add["mi_day_before"]
    MY_daily_add["mylr"] = MY_daily_add["mylr"] * MY_daily_add["mi_day_before"]
    MY_daily_add["myrr"] = MY_daily_add["myrr"] * MY_daily_add["mi_day_before"]

    # combine both tables and lose unnecessary information
    # df_milking contains the data of milking sessions of the current day (full MI on current day & proportion produced on current day of 'overnight' MI)
    # df_milking_add contains data of milking sessions of the previous day (proportion produced on previous day of 'overnight' MI)
    milking = pd.concat([milking, MY_daily_add])
    milking = milking[
        [
            "farm_id",
            "animal_id",
            "lactation_id",
            "parity",
            "mi",
            "dim_floor",
            "tmy",
            "mylf",
            "myrf",
            "mylr",
            "myrr",
            "mi_day_before",
            "mi_on_day",
        ]
    ]
    del MY_daily_add

    # multiply the mi with the proportion of each day to get the true values of mi per period
    # In df_milking (contains current day info): mi_day_before is always 0, mi_on_day is either 1 (full MI on current day) or smaller than 1 (proportion produced on current day of 'overnight' MI)
    # In df_milking_add (contains previous day): mi_on_day is always 0, mi_day_before lies between 0 and 1 (proportion produced on previous day)
    milking["mi"] = milking["mi"] * (milking["mi_day_before"] + milking["mi_on_day"])

    # group by dim_floor to get the daily milk yields. Add all measurements to the assigned day
    MY_daily = milking.groupby(
        ["farm_id", "animal_id", "lactation_id", "parity", "dim_floor"], dropna=False
    ).sum()
    MY_daily.reset_index(inplace=True)
    MY_daily = MY_daily.rename(
        columns={
            "dim_floor": "dim",
            "tmy": "tdmy",
            "mylf": "dmylf",
            "myrf": "dmyrf",
            "mylr": "dmylr",
            "myrr": "dmyrr",
        }
    )
    del milking

    # add 1 to dim to avoid errors during the fitting process (allow any y offset, might cause problems if y=0 in some models)
    MY_daily["dim"] += 1

    # correct the milk yields to true daily milk yield by deviding through the mi for each my calculation and multiply by 24h (correct for missing data)
    MY_daily["tdmy"] = (MY_daily["tdmy"] / MY_daily["mi"]) * 24
    MY_daily["dmylf"] = (MY_daily["dmylf"] / MY_daily["mi"]) * 24
    MY_daily["dmyrf"] = (MY_daily["dmyrf"] / MY_daily["mi"]) * 24
    MY_daily["dmylr"] = (MY_daily["dmylr"] / MY_daily["mi"]) * 24
    MY_daily["dmyrr"] = (MY_daily["dmyrr"] / MY_daily["mi"]) * 24

    MY_daily = MY_daily[
        [
            "farm_id",
            "animal_id",
            "lactation_id",
            "parity",
            "dim",
            "tdmy",
            "dmylf",
            "dmyrf",
            "dmylr",
            "dmyrr",
        ]
    ]

    # calculate a 7 day rolling median of the tdmy and select for tdmy values that are lower than
    # 1.5*the rolling median and below 75 kg daily milk yield
    MY_daily["tdmy7dm"] = MY_daily["tdmy"].rolling(7).median()
    MY_daily.loc[(MY_daily["dim"] < 7), "tdmy7dm"] = MY_daily.loc[
        (MY_daily["dim"] < 7), "tdmy"
    ]
    MY_daily = MY_daily[(MY_daily["tdmy"] < 1.5 * MY_daily["tdmy7dm"])]
    MY_daily = MY_daily[(MY_daily["tdmy"] < 75)]

    MY_daily = MY_daily[
        [
            "farm_id",
            "animal_id",
            "lactation_id",
            "parity",
            "dim",
            "tdmy",
            "dmylf",
            "dmyrf",
            "dmylr",
            "dmyrr",
        ]
    ]

    return MY_daily


# %% function 1: Wood


def wood(dim, a, b, c):
    """
    Defines the (non-linear) Wood model as y = p1 * np.power(x,p2) * np.exp(-p3*x)

    Parameters
    ----------
    dim : Array (dtype = float)
        Contains the DIM values of each milking session within one (quarter or udder level) lactation
    a : float
        First parameter: represents the milk yield right after calving (the intercept).
        Boundaries: [0 60 or 30]
        Usual offset values: depend on quarter/udder level. Often taking the mean value of the y variable
    b : float
        Second parameter: represents the decreasing part of the lactation curve (after the production peak).
        Boundaries:  [0 0.6]
        Usual offset values: 0.2
    c : float
        Third parameter: represents the increasing part of the lactation curve (before the production peak).
        Boundaries:  [0 0.01]
        Usual offset values: 0.005

    Returns
    -------
    y : Array (dtype = float)
        Predicted standardised daily milk yields of each milking session within one (quarter or udder level) lactation.

    """

    y = a * np.power(dim, b) * np.exp(-c * dim)

    return y


def woodres(dim, a, b, c, dmy):
    """
    Calculates the wood model (Wood model as y = p1 * np.power(x,p2) * np.exp(-p3*x)) and calculates the milk yield residuals between
    the measured milk yield and the model data

    Parameters
    ----------
    dim : Array (dtype = float)
        Contains the DIM values of each milking session within one (quarter or udder level) lactation
    a : float
        First parameter: represents the milk yield right after calving (the intercept).
        Boundaries: [0 60 or 30]
        Usual offset values: depend on quarter/udder level. Often taking the mean value of the y variable
    b : float
        Second parameter: represents the decreasing part of the lactation curve (after the production peak).
        Boundaries:  [0 0.6]
        Usual offset values: 0.2
    c : float
        Third parameter: represents the increasing part of the lactation curve (before the production peak).
        Boundaries:  [0 0.01]
        Usual offset values: 0.005
    dmy: Array (dtype = float)
        Contains the DMY values of each milking session within one (quarter or udder level) lactation

    Returns
    -------
    y : Array (dtype = float)
        Predicted standardised daily milk yields of each milking session within one (quarter or udder level) lactation.

    """

    y = wood(dim, a, b, c)
    res = dmy - y

    return res


def itw(
    dim,
    dmy,
    woodsettings={"init": [15, 0.25, 0.003], "lb": [0, 0, 0], "ub": [100, 5, 1]},
    iter_max=20,
    rmse_thr=0.1,
    plotbool=False,
):
    """
    Calculates the wood model (Wood model as y = p1 * np.power(x,p2) * np.exp(-p3*x)) iteratively, for each run, all values
    lower than 1.6 standard deviation below the mean are removed for the next iteration of fitting the wood function.
    The iterative process is either stopped after running for a certain number of iterations (iter_max) or when the
    change in rmse is below a certain threshold (rmse_thr). Inital boundary conditions, lower bounds and upper bounds can
    be given by:
    woodsettings = {"init" : [35,0.25,0.003],   # initial values
                    "lb" : [0,0,0],             # lowerbound
                    "ub" : [100,5,1],           # upperbound
                    }


    Parameters
    ----------
    dim : Array (dtype = float)
        Contains the DIM values of each milking session within one (quarter or udder level) lactation
    dmy : Array (dtype = float)
        Contains the DMY values of each milking session within one (quarter or udder level) lactation
    woodsettings : dict
        init = initial values for the wood model fit
        lb = lower boundaries
        ub = upper boundaries
        e.g., {"init" : [35,0.25,0.003],   # initial values
        "lb" : [0,0,0],             # lowerbound
        "ub" : [100,5,1],           # upperbound
        }
    iter_max : int
        Number of maximum iterations for the wood model fit
    rmse_thr : float
        Number of minimum change in rmse before the iterative process is discontinued
    plotbool: bool
        If true, create a plot of the fitting process

    Returns
    -------
    model : Array (dtype = float)
        Expected milk yield predicted by the final wood model
    model_parameter : Array
        Model parameters for the final applied wood curve

    """

    df = pd.DataFrame({"dim": dim, "dmy": dmy})

    # find initial fit of the wood model
    model_parameter = curve_fit(
        wood,
        dim,
        dmy,
        p0=woodsettings["init"],
        bounds=(woodsettings["lb"], woodsettings["ub"]),
        method="trf",
    )
    a = model_parameter[0][0]
    b = model_parameter[0][1]
    c = model_parameter[0][2]

    # calculate residuals and find (robust) std
    res = woodres(dim, a, b, c, dmy)
    try:
        sd = huber(res)[1]  # robust sd
    except:
        sd = res.std()
    mod = wood(dim, a, b, c)  # fitted wood model
    # t = mod - 1.6 * sd      # threshold
    t = mod - 0.6 * sd  # threshold

    # find all residuals below threshold of 1.6*sd
    idx_excl = dmy.loc[(dim > 7) & (dmy < t)].index.values

    # all residuals included (above the threshold)
    idx = dmy.loc[(dim <= 7) | (dmy >= t)].index.values

    # --------------------------------------------------------------------------
    if plotbool == True:
        # plots
        fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(20, 9))
        sns.lineplot(data=df, x="dim", y="dmy", color="blue", marker="o", ms=4, lw=1.2)
        ax.plot(
            dim,
            wood(
                dim,
                woodsettings["init"][0],
                woodsettings["init"][1],
                woodsettings["init"][2],
            ),
            color="grey",
            linestyle="--",
            lw=0.8,
        )
        ax.plot(dim, mod, color="firebrick", linestyle="--", lw=1.8)
        ax.plot(dim, t, color="red", linestyle=":", lw=0.4)
        ax.plot(
            dim[idx_excl], dmy[idx_excl], color="red", marker="x", lw=0, ls="", ms=3
        )

        ax.legend(labels=["dmy", "_", "init", "wood1", "threshold1", "_"])
    # --------------------------------------------------------------------------

    # prepare iterative procedure
    rmse0 = np.sqrt((res * res).mean())  # difference with prev needs to be > 0.10
    rmse1 = rmse0 + 1  # fictive value to start iterations
    no_iter = 0  # needs to be smaller than 20
    lendata = len(idx)  # needs to be larger than 50

    while (lendata > 50) and (no_iter < iter_max) and (rmse1 - rmse0 > rmse_thr):

        # add to no_iter
        no_iter = no_iter + 1
        print("iter = " + str(no_iter))

        # fit model on remaining data, with initial values = a,b,c
        model_parameter = curve_fit(
            wood,
            dim[idx],
            dmy[idx],
            p0=[a, b, c],
            bounds=(woodsettings["lb"], woodsettings["ub"]),
            method="trf",
        )
        a = model_parameter[0][0]
        b = model_parameter[0][1]
        c = model_parameter[0][2]

        # calculate residuals and find (robust) std
        res = woodres(dim, a, b, c, dmy)
        try:
            sd = huber(res)[1]  # robust sd
        except:
            sd = res.std()
        model = wood(dim, a, b, c)  # wood model fitted
        t = model - 1.6 * sd  # threshold

        # find all residuals below threshold of 1.6*sd
        idx_excl = dmy.loc[(dim > 7) & (dmy < t)].index.values

        # all residuals included (above the threshold)
        idx = dmy.loc[(dim <= 7) | (dmy >= t)].index.values

        # ----------------------------------------------------------------------
        if plotbool == True:

            ax.plot(dim, model, color="magenta", linestyle="--", lw=1)
            ax.plot(dim, t, color="magenta", linestyle=":", lw=0.4)
            ax.plot(
                dim[idx_excl], dmy[idx_excl], color="red", marker="x", lw=0, ls="", ms=3
            )
            if no_iter == 1:
                ax.legend(
                    labels=["dmy", "_", "init", "wood1", "threshold1", "_", "itw"]
                )
        # ----------------------------------------------------------------------

        # update criteria
        rmse1 = rmse0
        rmse0 = np.sqrt((res[idx] * res[idx]).mean())

        lendata = len(idx)

    print("no_iter = " + str(no_iter) + ", no_excluded = " + str(len(idx_excl)))
    if plotbool == True:

        ax.plot(dim, model, color="orangered", linestyle="-", lw=2)
        ax.set_ylabel("dmy [kg]")
        ax.set_xlabel("dim [d]")
        ax.set_title(
            "no_iter = " + str(no_iter) + ", no_excluded = " + str(len(idx_excl))
        )
    else:
        ax = None

    return model, model_parameter


def pert(dim, my, itw):
    """
    definitions perturbations:
        - If less than 5 days below ITW
                                                        no perturbation         [pert_severity = 0]
        - If >= 5 and less than 10	days below ITW
                never < 0.85*ITW		                very mild perturbation  [pert_severity = 1]
                1 or 2 days < 0.85*ITW				    mild perturbation       [pert_severity = 2]
                3 or more days < 0.85*ITW				moderate perturbation   [pert_severity = 3]
        - If more than 10 days below ITW
                0, 1 or 2 days < 0.85*ITW			    mild perturbation       [pert_severity = 2]
                3 or more days,
                    never >3 successive days	        moderate perturbation   [pert_severity = 3]
                3 or more days,
                    at least once >3 successive days    severe perturbation     [pert_severity = 4]
    Parameters
    ----------
    dim : Array (dtype = float)
        Contains the DIM values of each milking session within one (quarter or udder level) lactation
    my : Array (dtype = float)
        Contains the DMY values of each milking session within one (quarter or udder level) lactation
    itw : Array (dtype = float)
        Contains the DMY values of each milking session within one (quarter or udder level) lactation (given by e.g. 
        either the applied iterative wood model or the qreg model)

    Returns
    -------
    df : pd.DataFrame (dtype = float)
        Dataframe containing the input data, and 
            "res" : residuals between the real data (dmy) and the model (itw),
            "thres" : Threshold of 0.85*dmy, cutoff for perturbation definition,
            "pert_no" : Number of the perturbation in the lactation,
            "pert_dur" : Duration of each perturbation,
            "pert_low_count" : Count of days where the milk yield is below thres,
            "pert_severity" : Parameter defining the severity of the perturbation (description see above),
    
    """
    # create data frame and calculate model residuals
    df = pd.DataFrame({"dim": dim, "my": my, "mod": itw})

    df["res"] = df["my"] - df["mod"]
    df["thres"] = df["mod"] * 0.85

    # find std robust of residual time series
    try:
        sd = huber(df["res"])[1]  # robust sd
    except:
        sd = df["res"].std()

    # find negative
    df["is_neg"] = 0
    df.loc[df["my"] < df["mod"], "is_neg"] = 1

    # find below 1.6*robust_std
    df["is_low"] = 0
    df.loc[df["my"] < df["thres"], "is_low"] = 1

    # Step 1: Identify where 'is_neg' changes from the previous row
    df["change"] = df["is_neg"].ne(df["is_neg"].shift()).astype(int)

    # Step 2: Group consecutive rows
    df["group"] = df["change"].cumsum()
    df.group = (df.group + 1) / 2
    df.loc[df["group"] % 2 == 0.5, "group"] = 0

    # Step 3: Number periods of consecutive ones
    # This step is slightly modified to keep the group numbers for consecutive ones
    # and reset numbering for periods where 'is_neg' is 0.
    df["pert_no"] = (df["group"] * df["is_neg"]).astype(int)

    # Step 3: Count consecutive '1's for each group and assign back to rows where 'is_neg' is 1
    df["pert_dur"] = (
        df.groupby("group")["is_neg"].transform("sum") * df["is_neg"]
    ).astype(int)

    # Cleanup: Remove temporary columns if no longer needed
    df.drop(["change", "group"], axis=1, inplace=True)

    # Step 1: Group by 'pert_no' and calculate the count of rows where 'is_low' == 1 for each group
    df["pert_low_count"] = df.groupby("pert_no")["is_low"].transform(
        lambda x: (x == 1).sum()
    )

    # Step 1: Identify sequences of consecutive days where 'is_low' == 1 within each 'pert_no'
    df["is_low_change"] = df["is_low"].ne(df["is_low"].shift()) | df["pert_no"].ne(
        df["pert_no"].shift()
    )
    df["is_low_seq"] = df["is_low_change"].cumsum()

    # Step 2: Count the length of each sequence where 'is_low' == 1
    df["is_low_seq_len"] = df.groupby("is_low_seq")["is_low"].transform("sum")

    # Step 3: Determine if each 'pert_no' has at least one sequence of 3 or more consecutive 'is_low' == 1
    df["has_3_consec_low"] = df.groupby("pert_no")["is_low_seq_len"].transform(
        lambda x: (x >= 3).any()
    )

    # Cleanup: Remove temporary columns if no longer needed
    df.drop(["is_low_change", "is_low_seq", "is_low_seq_len"], axis=1, inplace=True)

    df.loc[(df.pert_dur < 5), "pert_severity"] = 0
    df.loc[
        (df.pert_dur >= 5) & (df.pert_dur < 10) & (df.pert_low_count == 0),
        "pert_severity",
    ] = 1
    df.loc[
        (df.pert_dur >= 5)
        & (df.pert_dur < 10)
        & (df.pert_low_count >= 1)
        & (df.pert_low_count <= 2),
        "pert_severity",
    ] = 2
    df.loc[
        (df.pert_dur >= 5) & (df.pert_dur < 10) & (df.pert_low_count >= 3),
        "pert_severity",
    ] = 3
    df.loc[(df.pert_dur >= 10) & (df.pert_low_count <= 2), "pert_severity"] = 2
    df.loc[
        (df.pert_dur >= 10) & (df.pert_low_count >= 3) & (df.has_3_consec_low == False),
        "pert_severity",
    ] = 3
    df.loc[
        (df.pert_dur >= 10) & (df.pert_low_count >= 3) & (df.has_3_consec_low == True),
        "pert_severity",
    ] = 4

    # Cleanup: Remove temporary columns if no longer needed
    df.drop(["has_3_consec_low"], axis=1, inplace=True)

    df.pert_severity = df.pert_severity.astype(int)

    return df[
        [
            "dim",
            "my",
            "mod",
            "res",
            "thres",
            "pert_no",
            "pert_dur",
            "pert_low_count",
            "pert_severity",
        ]
    ]


# function to define the loss function of quantile regression in a linear programming way
# give more weight to first 15 days.
def qreg(order, X, y, n_diff, tau1, tau2, plotbool):
    """
        quantile regression with number of x values fixed = first ndiff days
        in a seperate tau1

    tau1 = first tau =  quantile for first n_diff measurements (e.g. 0.1)
    tau2 = second tau = quantile for len(X)-n measurements (e.g. 0.7)

    resources:
    https://github.com/iadriaens/quantileRegression/blob/master/quantreg.m
    https://github.com/antononcube/MathematicaForPrediction/blob/master/Documentation/Quantile%20regression%20through%20linear%20programming.pdf
    https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.linprog.html
    https://nl.mathworks.com/help/optim/ug/linprog.html

    Parameters
    ----------
    order : int
        Order of polynomial function to use in the regression
    X : Array (dtype = float)
        Contains the DIM values of each milking session within one (quarter or udder level) lactation
    y : Array (dtype = float)
        Contains the DMY values of each milking session within one (quarter or udder level) lactation
    n_diff : int
        Number of days to which tau1 should be applied
    tau1 : float
        first tau =  quantile for first n_diff measurements (e.g. 0.1)
    tau2 : float 
        second tau = quantile for len(X)-n measurements (e.g. 0.7)
    plotbool : bool
        If true, create a plot of the fitting process

    Returns
    -------
    model : Array (dtype = float)
        Expected milk yield predicted by the qreg model
    model_parameter : Array
        Model parameters for the applied qreg

    """

    # convert X to matrix
    x = pd.DataFrame(X, columns=["dim"])
    x["ones"] = np.ones(len(x))
    x = x[["ones", "dim"]]
    if order > 1:
        for i in range(2, order + 1):
            # print(i)
            name = ["dim" + str(i)]
            x = pd.concat(
                [x, pd.DataFrame(data=X.values**i, columns=name, index=X.index)], axis=1
            )

    # sizes to create matrices
    n = len(x)
    m = order + 1

    # define function to optimize: equality constraints belonging to quantile regression (Aeq*x=beq)
    Aeq = np.block([np.eye(n), -np.eye(n), x])  # (n * 2n+m) linear equality constraints
    beq = y
    lb = np.hstack([np.zeros(n), np.zeros(n), -np.inf * np.ones(m)])
    ub = np.inf * np.ones(m + 2 * n)
    bounds = np.vstack([lb, ub]).T

    # # define function vector with quantiles as the objective function = normal qreg
    # f = np.hstack([tau2*np.ones(n),(1-tau2)*np.ones(n),np.zeros(m)])
    dimdiff = n_diff
    n_diff = sum(X < n_diff)

    # adjusted qreg objective function
    f = np.hstack(
        [
            tau1 * np.ones(n_diff),
            tau2 * np.ones(n - n_diff),
            (1 - tau1) * np.ones(n_diff),
            (1 - tau2) * np.ones(n - n_diff),
            np.zeros(m),
        ]
    )

    # solve linear program -- normal qreg
    out = linprog(f, A_eq=Aeq, b_eq=beq, bounds=bounds)
    model_parameter = out.x[-m:]

    # # solve linear program -- adjusted qreg
    # out2 = linprog(f2, A_eq=Aeq, b_eq=beq,bounds=bounds)
    # bhat2 = out2.x[-m:]

    if plotbool == True:
        # plot
        _, ax = plt.subplots(1, 1, figsize=(12, 6))
        plt.plot(X, y, "o-", color="darkblue", ms=4, label="data")
        # plt.plot(X,np.dot(x,bhat),"red",lw=1.5, label="qreg " + "\u03C4" +"$_1$" +" = " + str(tau2) )
        plt.plot(
            X,
            np.dot(x, model_parameter),
            "--",
            lw=2.5,
            color="red",
            label="qreg "
            + "\u03C4"
            + "$_1$"
            + " = "
            + str(tau1)
            + ", "
            + "\u03C4"
            + "$_2$"
            + " = "
            + str(tau2),
        )
        plt.legend()
        ax.set_xlabel("dim")
        ax.set_ylabel("dmy")
        ax.set_title(
            "quantile regression model, dim < "
            + str(dimdiff)
            + " have different \u03C4, polynomial order = "
            + str(order)
        )
    else:
        ax = 0

    # create dataframe outputs with indices of orginal X
    model = pd.DataFrame(data=np.dot(x, model_parameter), columns=["mod"], index=X.index)

    return model, model_parameter

def calc_thi(temperature, rel_humidity):
    """

    THI calculation:
    THI = 1.8*T+32-((0.55-0.0055*rel_hum)*(1.8*T-26))

    Parameters
    ----------
    temperature : Array (dtype = float)
        Temperature in Celsius 
    rel_humidity : Array (dtype = float)
        Relative humidity in percentage

    Returns
    -------
    thi : Array (dtype = float)       

    """

    # calculate per hour thi
    thi = 1.8 * temperature + 32 - ((0.55 - 0.0055 * rel_humidity) * (1.8 * temperature - 26))
    return thi


def add_thi(weather_dataframe):
    """
    Parameters
    ----------
    weather_dataframe : dataframe 
        Dataframe containing temperature and humidityy data

    Returns
    -------
    weather_dataframe : dataframe
        Dataframe containing additionally a column with thi 

    """

    weather_dataframe['thi'] = calc_thi(weather_dataframe.temperature, weather_dataframe.humidity)
    return weather_dataframe

def add_lat(weather_dataframe):
    """
    Calculates the relative time of the day where the temperature is 
    1. >= 25 - high temperature
    2. <= 18 - low temperature
    (>18 & <25 is considered moderate temperature)

    A daily lagged accumulated temperature (lat) is then calculated as follows
    lat = (0.5 * (1-temp_hrs_low-temp_hrs_high) + 2 * temp_hrs_high)*24


    Parameters
    ----------
    weather_dataframe : dataframe 
        dataframe containing temperature data and datetime

    Returns
    -------
    df_weather_daily : dataframe
        Dataframe containing the number of measurements per day, the min and max temperature,
        the relative time per day where the temperature is low, respectively high, and the lat

    """

    df_weather = weather_dataframe[["farm_id", "datetime", "temperature"]].copy()
    df_weather["date"] = df_weather.datetime.dt.date
    df_weather["temp_ishigh"] = 0
    df_weather.loc[df_weather["temperature"] >= 25, "temp_ishigh"] = 1
    df_weather["temp_islow"] = 0
    df_weather.loc[df_weather["temperature"] <= 18, "temp_islow"] = 1

    df_weather_daily = (
        df_weather[["farm_id", "date", "temperature", "temp_ishigh", "temp_islow"]]
        .groupby(by=["farm_id", "date"])
        .agg(
            {
                "temperature": ["count", "min", "max"],
                "temp_ishigh": ["sum"],
                "temp_islow": ["sum"],
            }
        )
    ).reset_index()

    df_weather_daily.columns = df_weather_daily.columns.droplevel()
    df_weather_daily.columns = ["farm_id","date","no_meas","temp_min","temp_max","temp_hrs_high","temp_hrs_low"]

    df_weather_daily.temp_hrs_high = df_weather_daily.temp_hrs_high/df_weather_daily.no_meas
    df_weather_daily.temp_hrs_low = df_weather_daily.temp_hrs_low/df_weather_daily.no_meas

    # calculate new weather feature thi heat stressed per day = 0.5*hrs mod temp + 2* hrs high temp
    df_weather_daily["lat"] = (0.5 * (1-df_weather_daily["temp_hrs_low"]-df_weather_daily["temp_hrs_high"]) + \
        2 * df_weather_daily["temp_hrs_high"]) * 24
    return df_weather_daily