import logging
from datetime import datetime, timedelta
import csv


class Foreflight(object):

    def __init__(self, logbook, configuration):
        self.logger = logging.getLogger(__name__)
        self.logbook = logbook.content.decode("utf8")
        self.airports = configuration.airports
        self.flight_logs = self.__injest_logbook()
        self.destinations = self.__parse_airports()
        self.airport_visits = self.__reconcile_airports()
        

    def __str__(self):
        return "logs={}, destinations={}, airport_visits={}".format(self.flight_logs, self.destinations, self.airport_visits,)        

    def __injest_logbook(self):
        """
        Takes in the contents of the csv to something we can work with
        The logbook mixes multiple outputs in a single file so we first 
        need to get rid of the Aircraft Table (I'll regret this later, 
        I'm sure!) so we are left with just the "Flight Table"
        """

        raw_logbook = csv.reader(self.logbook.splitlines(), delimiter=',')
        logbook_list = list(raw_logbook)
        flight_keyword = "Flights Table"
        log_entries_end = sum(1 for row in logbook_list)
        found_entries = int(0)
        flight_entries = [] * log_entries_end
        search_counter = 0

        for line in logbook_list:
            if (found_entries == 1):        
                flight_entries.append(line)

            if (line[0] == flight_keyword and found_entries == 0):
                self.logger.debug("found start of flight logs at line {}".format(search_counter))
                found_entries = 1
            search_counter += 1 
        return flight_entries        

    def __parse_airports(self):
        """
        Given the entire list of flights, dedup and count unique visits to each destination for frequency
        """
        import pandas as pd 
        header_list = self.flight_logs.pop(0)
        logbook_df = pd.DataFrame(self.flight_logs, columns=header_list)
        destinations = dict(logbook_df['To'].value_counts())
        return destinations


    def __reconcile_airports(self):
        """
        Given list of airports that user has been to, apply to list of airports actually available on the map (pixel_map)
        """    
        airport_visits = [] * 2
        
        for airport in self.airports: 
            for destination in self.destinations:
                if airport == destination:
                    airport_visits.append({destination : self.destinations[destination]})
                    break
        return airport_visits
