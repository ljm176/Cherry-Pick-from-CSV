t_list = [['2', 'A1', '3', 'A1', '100'], ['2', 'A2', '3', 'A2', '100'], ['2', 'A3', '3', 'A3', '100'], ['2', 'A4', '3', 'A4', '100'], ['2', 'A5', '3', 'A5', '100'], ['2', 'A6', '3', 'A6', '100'], ['2', 'A7', '3', 'A7', '100'], ['2', 'A8', '3', 'A8', '100'], ['2', 'A9', '3', 'A9', '100'], ['2', 'A10', '3', 'A10', '100'], ['2', 'A11', '3', 'A11', '100'], ['2', 'A12', '3', 'A12', '100'], ['2', 'B1', '3', 'B1', '100'], ['2', 'B2', '3', 'B2', '100'], ['2', 'B3', '3', 'B3', '100'], ['2', 'B4', '3', 'B4', '100'], ['2', 'B5', '3', 'B5', '100'], ['2', 'B6', '3', 'B6', '100'], ['2', 'B7', '3', 'B7', '100'], ['2', 'B8', '3', 'B8', '100'], ['2', 'B9', '3', 'B9', '100'], ['5', 'A1', '3', 'B10', '100'], ['5', 'A2', '3', 'B11', '100'], ['5', 'A3', '3', 'B12', '100'], ['5', 'A4', '3', 'C1', '100'], ['5', 'A5', '3', 'C2', '100'], ['5', 'A6', '3', 'C3', '100'], ['5', 'A7', '3', 'C4', '100'], ['5', 'A8', '3', 'C5', '100'], ['5', 'A9', '3', 'C6', '100'], ['5', 'A10', '3', 'C7', '100'], ['5', 'A11', '3', 'C8', '100'], ['5', 'A12', '3', 'C9', '100'], ['5', 'B1', '3', 'C10', '100'], ['5', 'B2', '3', 'C11', '100'], ['5', 'B3', '3', 'C12', '100'], ['5', 'B4', '3', 'D1', '100'], ['5', 'B5', '3', 'D2', '100'], ['5', 'B6', '3', 'D3', '100'], ['5', 'B7', '3', 'D4', '100'], ['5', 'B8', '3', 'D5', '100'], ['5', 'B9', '3', 'D6', '100'], ['5', 'B10', '3', 'D7', '100'], ['5', 'B11', '3', 'D8', '100'], ['5', 'B12', '3', 'D9', '100'], ['5', 'C1', '3', 'D10', '100'], ['5', 'C2', '3', 'D11', '100'], ['5', 'C3', '3', 'D12', '100'], ['5', 'C4', '3', 'E1', '100'], ['5', 'C5', '3', 'E2', '100'], ['5', 'C6', '3', 'E3', '100'], ['5', 'C7', '3', 'E4', '100'], ['5', 'C8', '3', 'E5', '100'], ['5', 'C9', '3', 'E6', '100'], ['5', 'C10', '3', 'E7', '100'], ['5', 'C11', '3', 'E8', '100'], ['5', 'C12', '3', 'E9', '100'], ['5', 'D1', '3', 'E10', '100'], ['5', 'D2', '3', 'E11', '100'], ['5', 'D3', '3', 'E12', '100'], ['5', 'D4', '3', 'F1', '100'], ['5', 'D5', '3', 'F2', '100'], ['5', 'D6', '3', 'F3', '100'], ['5', 'D7', '3', 'F4', '100'], ['5', 'D8', '3', 'F5', '100'], ['5', 'D9', '3', 'F6', '100'], ['5', 'D10', '3', 'F7', '100'], ['5', 'D11', '3', 'F8', '100'], ['5', 'D12', '3', 'F9', '100'], ['5', 'E1', '3', 'F10', '100'], ['5', 'E2', '3', 'F11', '100'], ['5', 'E3', '3', 'F12', '100'], ['5', 'E4', '3', 'G1', '100'], ['5', 'E5', '3', 'G2', '100'], ['5', 'E6', '3', 'G3', '100'], ['5', 'E7', '3', 'G4', '100'], ['5', 'E8', '3', 'G5', '100'], ['5', 'E9', '3', 'G6', '100']]
metadata = {
    'protocolName': 'Generic Cherrypicking Transfer',
    'author': 'Lachlan',
    'source': 'Custom Protocol Request',
    'apiLevel': '2.2'
}

def run(protocol):
    #Load Tips
    
    tips200 = [protocol.load_labware('opentrons_96_tiprack_300ul', 1)]

    #Load Pipettes
    
    p300Single = protocol.load_instrument('p300_single', 'left', tip_racks=tips200)

    rack = protocol.load_labware("opentrons_6_tuberack_falcon_50ml_conical", 9)
    glycerol = rack.wells_by_name()["A1"]


    source_plate =  "usascientific_96_wellplate_2.4ml_deep"
    dest_plate = "biorad_96_wellplate_200ul_pcr"
    
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
        p300Single.consolidate([100, float(vol)], [glycerol, source], dest, mix_after=(3, 200))
    
    for transfers in t_list:
        pick(transfers)
    