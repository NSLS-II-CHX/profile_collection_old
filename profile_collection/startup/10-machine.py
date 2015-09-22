from ophyd.controls import PVPositioner

# Undulator
ivu_gap = PVPositioner('SR:C11-ID:G1{IVU20:1-Mtr:2}Inp:Pos',
			readback='SR:C11-ID:G1{IVU20:1-LEnc}Gap',
			act='SR:C11-ID:G1{IVU20:1-Mtr:2}Sw:Go',
			act_val=1,
			stop='SR:C11-ID:G1{IVU20:1-Mtr:2}Pos.STOP',
			stop_val=1,
			put_complete=True,
			name='ivu_gap'
		       )
# Front End Slits (Primary Slits)

fe_xc = PVPositioner('FE:C11A-OP{Slt:12-Ax:X}center',
                     readback='FE:C11A-OP{Slt:12-Ax:X}t2.D',
                     stop='FE:C11A-CT{MC:1}allstop',
                     stop_val=1, put_complete=True,
                     name='fe_xc')

fe_yc = PVPositioner('FE:C11A-OP{Slt:12-Ax:Y}center',
                     readback='FE:C11A-OP{Slt:12-Ax:Y}t2.D',
                     stop='FE:C11A-CT{MC:1}allstop',
                     stop_val=1,
                     put_complete=True,
                     name='fe_yc')

fe_xg = PVPositioner('FE:C11A-OP{Slt:12-Ax:X}size',
                     readback='FE:C11A-OP{Slt:12-Ax:X}t2.C',
                     stop='FE:C11A-CT{MC:1}allstop',
                     stop_val=1, put_complete=True,
                     name='fe_xg')

fe_yg = PVPositioner('FE:C11A-OP{Slt:12-Ax:Y}size',
                     readback='FE:C11A-OP{Slt:12-Ax:Y}t2.C',
                     stop='FE:C11A-CT{MC:1}allstop',
                     stop_val=1,
                     put_complete=True,
                     name='fe_yg')
