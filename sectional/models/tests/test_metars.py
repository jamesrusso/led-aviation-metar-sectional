# Free for personal use. Prohibited from commercial use without consent.
from sectional.models import Metar, AirportCondition
import unittest

class MetarTests(unittest.TestCase):

    def test_ceilings(self):
        x = Metar("KRNT 132053Z 33010KT 10SM SCT034 SCT041 23/14 A3001 RMK AO2 SLP165")
        self.assertEqual(x.ceiling, 10000)
        x = Metar("KRNT 132053Z 33010KT 10SM SCT034 SCT041 23/14 A3001 RMK AO2 SLP165")
        self.assertEqual(x.ceiling, 10000)
        x = Metar('KRNT 132053Z 33010KT 10SM SCT034 SCT041 23/14 A3001 RMK AO2 SLP165')
        self.assertEqual(x.ceiling, 10000)
        x = Metar('KRNT 132053Z 33010KT 4SM BKN041 SCT030 23/14 A3001 RMK AO2 SLP165')
        self.assertEqual(x.ceiling, 4100)        
        x = Metar('KRNT 132053Z 33010KT 4SM BKN041 OVC030 23/14 A3001 RMK AO2 SLP165')
        self.assertEqual(x.ceiling, 3000)   
        x = Metar('KRNT 132053Z 33010KT 4SM SCT041 OVC030 23/14 A3001 RMK AO2 SLP165')
        self.assertEqual(x.ceiling, 3000)   
        x = Metar('KRNT 132053Z 33010KT 3SM SCT041 BKN025 23/14 A3001 RMK AO2 SLP165')
        self.assertEqual(x.ceiling, 2500)   
        x = Metar('KRNT 132053Z 33010KT 2 1/2SM SCT041 BKN009 23/14 A3001 RMK AO2 SLP165')
        self.assertEqual(x.ceiling, 900)   
        x = Metar('KRNT 132053Z 33010KT 2 1/2SM SCT041 OVC009 23/14 A3001 RMK AO2 SLP165')
        self.assertEqual(x.ceiling, 900)   
        x = Metar('KRNT 132053Z 33010KT 2SM OVC004 23/14 A3001 RMK AO2 SLP165')
        self.assertEqual(x.ceiling, 400)   
        x = Metar('KRNT 132053Z 33010KT 2SM SCT010 OVC004 23/14 A3001 RMK AO2 SLP165')
        self.assertEqual(x.ceiling, 400)   
        x = Metar('KGCC 231853Z AUTO 28011KT 20/12 A2991 RMK AO2 LTG DSNT SE RAB41RAEMM SLP085 P0000 T02000117 PWINO $')
        self.assertEqual(x.ceiling, 10000)   
        x = Metar('KVOK 251453Z 34004KT 10SM SCT008 OVC019 21/21 A2988 RMK AO2A SCT V BKN SLP119 53012')
        self.assertEqual(x.ceiling, 1900)   
    
    def test_ceiling_classifications(self):
        x = Metar('KRNT 132053Z 33010KT 10SM SCT034 SCT041 23/14 A3001 RMK AO2 SLP165')
        self.assertEqual(x.ceiling_category, AirportCondition.VFR)
        x = Metar('KRNT 132053Z 33010KT 10SM SCT034 SCT041 23/14 A3001 RMK AO2 SLP165')
        self.assertEqual(x.ceiling_category, AirportCondition.VFR)
        x = Metar('KRNT 132053Z 33010KT 4SM SCT041 OVC030 23/14 A3001 RMK AO2 SLP165')
        self.assertEqual(x.ceiling_category, AirportCondition.VFR)
        x = Metar('KRNT 132053Z 33010KT 3SM SCT041 BKN025 23/14 A3001 RMK AO2 SLP165')
        self.assertEqual(x.ceiling_category, AirportCondition.MVFR)
        x = Metar('KRNT 132053Z 33010KT 2 1/2SM SCT041 BKN009 23/14 A3001 RMK AO2 SLP165')
        self.assertEqual(x.ceiling_category, AirportCondition.IFR)
        x = Metar('KRNT 132053Z 33010KT 2 1/2SM SCT041 OVC009 23/14 A3001 RMK AO2 SLP165')
        self.assertEqual(x.ceiling_category, AirportCondition.IFR)
        x = Metar('KRNT 132053Z 33010KT 2SM OVC004 23/14 A3001 RMK AO2 SLP165')
        self.assertEqual(x.ceiling_category, AirportCondition.LIFR)
        x = Metar('KRNT 132053Z 33010KT 2SM SCT010 OVC004 23/14 A3001 RMK AO2 SLP165')
        self.assertEqual(x.ceiling_category, AirportCondition.LIFR)
        x = Metar('KGCC 231853Z AUTO 28011KT 20/12 A2991 RMK AO2 LTG DSNT SE RAB41RAEMM SLP085 P0000 T02000117 PWINO $')
        self.assertEqual(x.ceiling_category, AirportCondition.VFR)
        x = Metar('KVOK 251453Z 34004KT 10SM SCT008 OVC019 21/21 A2988 RMK AO2A SCT V BKN SLP119 53012')
        self.assertEqual(x.ceiling_category, AirportCondition.MVFR)

def get_visibility(self):
      x = Metar('KRNT 132053Z 33010KT 10SM SCT034 SCT041 23/14 A3001 RMK AO2 SLP165')
      self.assertEqual(x.ceiling_category, AirportCondition.VFR)
      x = Metar('KRNT 132053Z 33010KT 4SM SCT034 SCT041 23/14 A3001 RMK AO2 SLP165')
      self.assertEqual(x.ceiling_category, AirportCondition.MVFR)
      x = Metar('KRNT 132053Z 33010KT 3SM SCT034 SCT041 23/14 A3001 RMK AO2 SLP165')
      self.assertEqual(x.ceiling_category, AirportCondition.MVFR)
      x = Metar('KRNT 132053Z 33010KT 2 1/2SM SCT034 SCT041 23/14 A3001 RMK AO2 SLP165')
      self.assertEqual(x.ceiling_category, AirportCondition.IFR)
      x = Metar('KRNT 132053Z 33010KT 2SM SCT034 SCT041 23/14 A3001 RMK AO2 SLP165')
      self.assertEqual(x.ceiling_category, AirportCondition.IFR)
      x = Metar('KRNT 132053Z 33010KT 1SM SCT034 SCT041 23/14 A3001 RMK AO2 SLP165')
      self.assertEqual(x.ceiling_category, AirportCondition.IFR)
      x = Metar('KRNT 132053Z 33010KT 1/2SM SCT034 SCT041 23/14 A3001 RMK AO2 SLP165')
      self.assertEqual(x.ceiling_category, AirportCondition.LIFR)
      x = Metar('KGCC 231853Z AUTO 28011KT 20/12 A2991 RMK AO2 LTG DSNT SE RAB41RAEMM SLP085 P0000 T02000117 PWINO $')
      self.assertEqual(x.ceiling_category, AirportCondition.VFR)
      x = Metar('KVOK 251453Z 34004KT 10SM SCT008 OVC019 21/21 A2988 RMK AO2A SCT V BKN SLP119 53012')
      self.assertEqual(x.ceiling_category, AirportCondition.VFR)