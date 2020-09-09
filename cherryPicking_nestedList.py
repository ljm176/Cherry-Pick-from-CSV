# -*- coding: utf-8 -*-
"""
Created on Wed Sep  9 09:00:54 2020

@author: lajamu
"""
t_list = [[5, "A3", 6, "A1", 20], [7, "B6", 6, "B1", 12]]
source_plate = "corning_96_wellplate_360ul_flat"
dest_plate = "corning_96_wellplate_360ul_flat"


metadata = {
    'protocolName': 'Generic Cherrypicking Transfer',
    'author': 'Lachlan',
    'source': 'Custom Protocol Request',
    'apiLevel': '2.2'
}




#def load_labware(ind):
#        occupied_slots = [transfer_step[ind] for transfer_step in t_list]
#        print(occupied_slots)



def run(protocol):
    #Load Tips
    tips20= [protocol.load_labware('opentrons_96_tiprack_20ul', '1')]
    tips200 = [protocol.load_labware('opentrons_96_tiprack_300ul', '2')]

    #Load Pipettes
    p20Single = protocol.load_instrument('p20_single_gen2', 'right', tip_racks=tips20)
    p300Single = protocol.load_instrument('p300_single', 'left', tip_racks=tips200)
    
    def load_labware(ind, plate):
        occupied_slots = [transfer_step[ind] for transfer_step in t_list]
        loaded= []
        for slot in occupied_slots:
            if slot not in loaded:
                protocol.load_labware(plate, str(slot))
                loaded.append(slot)
            
    load_labware(0, source_plate)
    load_labware(2, dest_plate)       
    
    def pick(l):
        source_plate, source_well, dest_plate, dest_well, vol = l
        source = protocol.loaded_labwares[int(source_plate)].wells_by_name()[source_well]
        dest = protocol.loaded_labwares[int(dest_plate)].wells_by_name()[dest_well]
        p20Single.transfer(float(vol), source, dest)
    
    for transfers in t_list:
        pick(transfers)
    