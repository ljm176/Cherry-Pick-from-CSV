t_list = [['4', 'A1', '6', 'A1', '100'], ['4', 'A2', '6', 'A2', '100'], ['4', 'A3', '6', 'A3', '100'], ['4', 'A4', '6', 'A4', '100'], ['4', 'A5', '6', 'A5', '100'], ['4', 'A6', '6', 'A6', '100'], ['4', 'A7', '6', 'A7', '100'], ['4', 'A8', '6', 'A8', '100'], ['4', 'A9', '6', 'A9', '100'], ['4', 'A10', '6', 'A10', '100'], ['4', 'A11', '6', 'A11', '100'], ['4', 'A12', '6', 'A12', '100'], ['4', 'B1', '6', 'B1', '100'], ['4', 'B2', '6', 'B2', '100'], ['4', 'B3', '6', 'B3', '100'], ['4', 'B4', '6', 'B4', '100'], ['4', 'B5', '6', 'B5', '100'], ['4', 'B6', '6', 'B6', '100'], ['4', 'B7', '6', 'B7', '100'], ['4', 'B8', '6', 'B8', '100'], ['4', 'B9', '6', 'B9', '100'], ['5', 'A1', '6', 'B10', '100'], ['5', 'A2', '6', 'B11', '100'], ['5', 'A3', '6', 'B12', '100'], ['5', 'A4', '6', 'C1', '100'], ['5', 'A5', '6', 'C2', '100'], ['5', 'A6', '6', 'C3', '100'], ['5', 'A7', '6', 'C4', '100'], ['5', 'A8', '6', 'C5', '100'], ['5', 'A9', '6', 'C6', '100'], ['5', 'A10', '6', 'C7', '100'], ['5', 'A11', '6', 'C8', '100'], ['5', 'A12', '6', 'C9', '100'], ['5', 'B1', '6', 'C10', '100'], ['5', 'B2', '6', 'C11', '100'], ['5', 'B3', '6', 'C12', '100'], ['5', 'B4', '6', 'D1', '100'], ['5', 'B5', '6', 'D2', '100'], ['5', 'B6', '6', 'D3', '100'], ['5', 'B7', '6', 'D4', '100'], ['5', 'B8', '6', 'D5', '100'], ['5', 'B9', '6', 'D6', '100'], ['5', 'B10', '6', 'D7', '100'], ['5', 'B11', '6', 'D8', '100'], ['5', 'B12', '6', 'D9', '100'], ['5', 'C1', '6', 'D10', '100'], ['5', 'C2', '6', 'D11', '100'], ['5', 'C3', '6', 'D12', '100'], ['5', 'C4', '6', 'E1', '100'], ['5', 'C5', '6', 'E2', '100'], ['5', 'C6', '6', 'E3', '100'], ['5', 'C7', '6', 'E4', '100'], ['5', 'C8', '6', 'E5', '100'], ['5', 'C9', '6', 'E6', '100'], ['5', 'C10', '6', 'E7', '100'], ['5', 'C11', '6', 'E8', '100'], ['5', 'C12', '6', 'E9', '100'], ['5', 'D1', '6', 'E10', '100'], ['5', 'D2', '6', 'E11', '100'], ['5', 'D3', '6', 'E12', '100'], ['5', 'D4', '6', 'F1', '100'], ['5', 'D5', '6', 'F2', '100'], ['5', 'D6', '6', 'F3', '100'], ['5', 'D7', '6', 'F4', '100'], ['5', 'D8', '6', 'F5', '100'], ['5', 'D9', '6', 'F6', '100'], ['5', 'D10', '6', 'F7', '100'], ['5', 'D11', '6', 'F8', '100'], ['5', 'D12', '6', 'F9', '100'], ['5', 'E1', '6', 'F10', '100'], ['5', 'E2', '6', 'F11', '100'], ['5', 'E3', '6', 'F12', '100'], ['5', 'E4', '6', 'G1', '100'], ['5', 'E5', '6', 'G2', '100'], ['5', 'E6', '6', 'G3', '100'], ['5', 'E7', '6', 'G4', '100'], ['5', 'E8', '6', 'G5', '100'], ['5', 'E9', '6', 'G6', '100']]
metadata = {
    'protocolName': 'Generic Cherrypicking Transfer',
    'author': 'Lachlan',
    'source': 'Custom Protocol Request',
    'apiLevel': '2.2'
}

def run(protocol):
    #Load Tips
    tips20= [protocol.load_labware('opentrons_96_tiprack_20ul', '1')]
    tips200 = [protocol.load_labware('opentrons_96_tiprack_300ul', '2')]

    #Load Pipettes
    p20Single = protocol.load_instrument('p20_single_gen2', 'right', tip_racks=tips20)
    p300Single = protocol.load_instrument('p300_single', 'left', tip_racks=tips200)

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
        p20Single.transfer(float(vol), source, dest)
    
    for transfers in t_list:
        pick(transfers)
    