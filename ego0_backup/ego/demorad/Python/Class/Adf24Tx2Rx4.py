# ADF24Tx2RX8 -- Class for 24-GHz Radar
#
# Copyright (C) 2015-11 Inras GmbH Haderer Andreas
# All rights reserved.
#
# This software may be modified and distributed under the terms
# of the BSD license.  See the LICENSE file for details.

import  Class.DevAdf5904  as DevAdf5904
import  Class.DevAdf5901  as DevAdf5901
import  Class.DevAdf4159  as DevAdf4159
import  Class.DemoRad     as DemoRad
from    numpy import *

class Adf24Tx2Rx4(DemoRad.DemoRad):

    def __init__(self):
        # Call Constructor of DemoRad Class
        super().__init__()
        self.DebugInf                   =   21
        #>  Object of first receiver (DevAdf5904 class object)
        self.Adf_Rx                =   []
        #>  Object of transmitter (DevAdf5901 class object)
        self.Adf_Tx                 =   []
        #>  Object of transmitter Pll (DevAdf4159 class object)
        self.Adf_Pll                    =   []

        self.Rf_USpiCfg_Mask            =   1
        self.Rf_USpiCfg_Pll_Chn         =   2
        self.Rf_USpiCfg_Tx_Chn          =   1
        self.Rf_USpiCfg_Rx_Chn          =   0

        self.Rf_Adf5904_FreqStrt        =   24.125e9
        self.Rf_Adf5904_RefDiv          =   1
        self.Rf_Adf5904_SysClk          =   80e6

        self.Rf_fStrt                   =   76e9
        self.Rf_fStop                   =   77e9
        self.Rf_TRampUp                 =   256e-6
        self.Rf_TRampDo                 =   256e-6
        self.Rf_fs                      =   1.0e6

        self.Rf_VcoDiv                  =   2

        self.stRfVers                   =   '2.0.1'

        self.StrtIdx                    =   0
        self.StopIdx                    =   1

        # Initialize Receiver

        dUSpiCfg                        =   dict()
        dUSpiCfg                        =   {   "Mask"          : self.Rf_USpiCfg_Mask,
                                                "Chn"           : self.Rf_USpiCfg_Rx_Chn
                                            }
        self.Adf_Rx = DevAdf5904.DevAdf5904(self, dUSpiCfg)
        dUSpiCfg                        =   dict()
        dUSpiCfg                        =   {   "Mask"          : self.Rf_USpiCfg_Mask,
                                                "Chn"           : self.Rf_USpiCfg_Tx_Chn
                                            }

        self.Adf_Tx                     =   DevAdf5901.DevAdf5901(self, dUSpiCfg)

        dUSpiCfg                        =   dict()
        dUSpiCfg                        =   {   "Mask"          : self.Rf_USpiCfg_Mask,
                                                "Chn"           : self.Rf_USpiCfg_Pll_Chn
                                            }
        self.Adf_Pll                    =   DevAdf4159.DevAdf4159(self, dUSpiCfg)




    # DOXYGEN ------------------------------------------------------
    #> @brief Get Version information of Adf24Tx2Rx8 class
    #>
    #> Get version of class
    #>      - Version string is returned as string
    #>
    #> @return  Returns the version string of the class (e.g. 0.5.0)
    def     RfGetVers(self):
        return

    def     BrdGetData(self):
        return self.Dsp_GetChirp(self.StrtIdx,self.StopIdx)

    def     RfGetChipSts(self):
        lChip   =   list()
        Val     =   self.Fpga_GetRfChipSts(1)
        print(Val)
        if Val[0] == True:
            Val     =   Val[1]
            if len(Val) > 2:
                if Val[0] == 202:
                    lChip.append(('Adf4159 PLL', 'No chip information available'))
                    lChip.append(('Adf5901 TX', 'No chip information available'))
                    lChip.append(('Adf5904 RX', 'No chip information available'))
        return lChip

    # DOXYGEN ------------------------------------------------------
    #> @brief Set attribute of class object
    #>
    #> Sets different attributes of the class object
    #>
    #> @param[in]     stSel: String to select attribute
    #>
    #> @param[in]     Val: value of the attribute (optional); can be a string or a number
    #>
    #> Supported parameters
    #>              - Currently no set parameter supported
    def RfSet(self, *varargin):
        if len(varargin) > 0:
            stVal   =   varargin[0]

    # DOXYGEN ------------------------------------------------------
    #> @brief Get attribute of class object
    #>
    #> Reads back different attributs of the object
    #>
    #> @param[in]   stSel: String to select attribute
    #>
    #> @return      Val: value of the attribute (optional); can be a string or a number
    #>
    #> Supported parameters
    #>      -   <span style="color: #ff9900;"> 'TxPosn': </span> Array containing positions of Tx antennas
    #>      -   <span style="color: #ff9900;"> 'RxPosn': </span> Array containing positions of Rx antennas
    #>      -   <span style="color: #ff9900;"> 'ChnDelay': </span> Channel delay of receive channels
    def RfGet(self, *varargin):
        if len(varargin) > 0:
            stVal       = varargin[0]
            if stVal == 'TxPosn':
                Ret     =   zeros(2)
                Ret[0]  =   -18.654e-3
                Ret[1]  =   0.0e-3
                return Ret
            elif stVal == 'RxPosn':
                Ret     =   arange(4)
                Ret     =   Ret*6.2170e-3 + 32.014e-3
                return Ret
            elif stVal == 'B':
                Ret     =   (self.Rf_fStop - self.Rf_fStrt)
                return  Ret
            elif stVal == 'kf':
                Ret     =   (self.Rf_fStop - self.Rf_fStrt)/self.Rf_TRampUp
                return  Ret
            elif stVal == 'kfUp':
                Ret     =   (self.Rf_fStop - self.Rf_fStrt)/self.Rf_TRampUp
                return  Ret
            elif stVal == 'kfDo':
                Ret     =   (self.Rf_fStop - self.Rf_fStrt)/self.Rf_TRampDo
                return  Ret
            elif stVal == 'fc':
                Ret     =   (self.Rf_fStop + self.Rf_fStrt)/2
                return  Ret
            elif stVal == 'fs':
                Ret     =   self.Rf_fs
                return  Ret
        return -1

    # DOXYGEN ------------------------------------------------------
    #> @brief Enable all receive channels
    #>
    #> Enables all receive channels of frontend
    #>
    #>
    #> @note: This command calls the Adf4904 objects Adf_Rx
    #>        In the default configuration all Rx channels are enabled. The configuration of the objects can be changed before
    #>        calling the RxEna command.
    #>
    #> @code
    #> CfgRx1.Rx1      =   0;
    #> Brd.Adf_Rx1.SetCfg(CfgRx1);
    #> CfgRx2.All      =   0;
    #> Brd.Adf_Rx2.SetCfg(CfgRx2);
    #> @endcode
    #>  In the above example Chn1 of receiver 1 is disabled and all channels of receiver Rx2 are disabled
    def     RfRxEna(self):
        print("RfRxEna")
        self.RfAdf5904Ini(1);

    # DOXYGEN ------------------------------------------------------
    #> @brief Configure receivers
    #>
    #> Configures selected receivers
    #>
    #> @param[in]   Mask: select receiver: 1 receiver 1; 2 receiver 2
    #>
    def     RfAdf5904Ini(self, Mask):
        if Mask == 1:
            self.Adf_Rx.Ini();
            if self.DebugInf > 10:
                print('Rf Initialize Rx1 (ADF5904)')
        else:
            pass

    # DOXYGEN ------------------------------------------------------
    #> @brief Configure registers of receiver
    #>
    #> Configures registers of receivers
    #>
    #> @param[in]   Mask: select receiver: 1 receiver 1; 2 receiver 2
    #>
    #> @param[in]   Data: register values
    #>
    #> @note Function is obsolete in class version >= 1.0.0: use function Adf_Rx1.SetRegs() and Adf_Rx2.SetRegs() to configure receiver
    def     RfAdf5904SetRegs(self, Mask, Data):
        if Mask == 1:
            self.Adf_Rx.SetRegs(Data)
            if self.DebugInf > 10:
                print('Rf Initialize Rx (ADF5904)')
        else:
            pass

    # DOXYGEN ------------------------------------------------------
    #> @brief Configure registers of transmitter
    #>
    #> Configures registers of transmitter
    #>
    #> @param[in]   Mask: select receiver: 1 transmitter 1
    #>
    #> @param[in]   Data: register values
    #>
    #> @note Function is obsolete in class version >= 1.0.0: use function Adf_Tx.SetRegs() to configure transmitter
    def     RfAdf5901SetRegs(self, Mask, Data):
        if Mask == 1:
            self.Adf_Tx.SetRegs(Data)
            print('Rf Initialize Tx (ADF5901)')


        # DOXYGEN ------------------------------------------------------
    #> @brief Configure registers of PLL
    #>
    #> Configures registers of PLL
    #>
    #> @param[in]   Mask: select receiver: 1 transmitter 1
    #>
    #> @param[in]   Data: register values
    #>
    #> @note Function is obsolete in class version >= 1.0.0: use function Adf_Pll.SetRegs() to configure PLL
    def     RfAdf4159SetRegs(self, Mask, Data):
        Data                =   Data.flatten(1)

        dUSpiCfg["Mask"]    =   self.Rf_USpiCfg_Mask
        dUSpiCfg["Chn"]     =   self.Rf_USpiCfg_Pll_Chn
        Ret                 =   self.Fpga_SetUSpiData(dUSpiCfg, Data);
        return Ret

    # DOXYGEN -------------------------------------------------
    #> @brief Displays status of frontend in Matlab command window
    #>
    #> Display status of frontend in Matlab command window
    def     BrdDispSts(self):
        self.BrdDispInf()
        self.Fpga_DispRfChipSts(1)

    # DOXYGEN ------------------------------------------------------
    #> @brief Enable transmitter
    #>
    #> Configures TX device
    #>
    #> @param[in]   TxChn
    #>                  - 0: off
    #>                  - 1: Transmitter 1 on
    #>                  - 2: Transmitter 2 on
    #> @param[in]   TxPwr: Power register setting 0 - 256; only 0 to 100 has effect
    #>
    #>
    def     RfTxEna(self, TxChn, TxPwr):
        TxChn       =   (TxChn % 3)
        TxPwr       =   (TxPwr % 2**8)
        if self.DebugInf > 10:
            stOut   =   "Rf Initialize Tx (ADF5901): Chn: " + str(TxChn) + " | Pwr: " + str(TxPwr)
            print(stOut)
        dCfg            =   dict()
        dCfg["TxChn"]   =   TxChn
        dCfg["TxPwr"]   =   TxPwr
        self.Dsp_SetMimo(0)
        self.Adf_Tx.SetCfg(dCfg)
        self.Adf_Tx.Ini()


    def     RfMeas(self, *varargin):

        ErrCod      =   0
        if len(varargin) > 1:
            stMod       =   varargin[0]

            if stMod == 'Adi':

                print('Simple Measurement Mode: Analog Devices')
                dCfg            =   varargin[1]

                if not ('fStrt' in dCfg):
                    print('RfMeas: fStrt not specified!')
                    ErrCod      =   -1
                if not ('fStop' in dCfg):
                    print('RfMeas: fStop not specified!')
                    ErrCod      =   -1
                if not ('TRampUp' in dCfg):
                    print('RfMeas: TRampUp not specified!')
                    ErrCod      =   -1

                if 'StrtIdx' in dCfg:
                    self.StrtIdx    =   dCfg["StrtIdx"]
                if 'StopIdx' in dCfg:
                    self.StopIdx    =   dCfg["StopIdx"]

                print("fStrt: ", dCfg["fStrt"])
                print("fStop: ", dCfg["fStop"])


                fsSel                   =   array([1, 1.2, 1.8])*1e6
                if 'fs' in dCfg:
                    ClkSel              =   argmin(abs(fsSel - dCfg['fs']))
                    ClkInt              =   1/fsSel[ClkSel]
                    self.Rf_fs          =   dCfg['fs']
                else:
                    ClkSel              =   1
                    ClkInt              =   1e-6

                if ClkSel == 0:
                    self.ADR7251Cfg[6]  =   int('0x00010000',0) + 100
                    self.ADR7251Cfg[7]  =   int('0x00020000',0) + 76
                    self.ADR7251Cfg[8]  =   int('0x00032833',0)
                    self.ADR7251Cfg[9]  =   int('0x01400000',0) + 3
                elif ClkSel == 1:
                    self.ADR7251Cfg[6]  =   int('0x00010000',0) + 1000
                    self.ADR7251Cfg[7]  =   int('0x00020000',0) + 304
                    self.ADR7251Cfg[8]  =   int('0x00031003',0)
                    self.ADR7251Cfg[9]  =   int('0x01400000',0) + 3
                elif ClkSel == 2:
                    self.ADR7251Cfg[6]  =   int('0x00010000',0) + 1000
                    self.ADR7251Cfg[7]  =   int('0x00020000',0) + 304
                    self.ADR7251Cfg[8]  =   int('0x00031003',0)
                    self.ADR7251Cfg[9]  =   int('0x01400000',0) + 2
                else:
                    self.ADR7251Cfg[6]  =   int('0x00010000',0) + 100
                    self.ADR7251Cfg[7]  =   int('0x00020000',0) + 76
                    self.ADR7251Cfg[8]  =   int('0x00032833',0)
                    self.ADR7251Cfg[9]  =   int('0x01400000',0) + 3

                dCfg['ClkInt']          =   ClkInt
                dCfg['ClkSel']          =   ClkSel

                print('Sampling frequency: ', fsSel[ClkSel]/1e6, ' MSPS')
                # configure sampling clock to the timer unit
                self.ADIFMCWCfg[8]  =   ClkSel + 1

                self.Rf_fStrt           =   dCfg["fStrt"]
                self.Rf_fStop           =   dCfg["fStop"]
                self.Rf_TRampUp         =   floor(dCfg['TRampUp']/ClkInt)*ClkInt

                if self.Rf_TRampUp/ClkInt < 260:
                    disp('Adf24Tx2Rx4: Set TRampUp to 260 clock cycles')
                    self.Rf_TRampUp     =   260*ClkInt
                    dCfg['TRampUp']     =   260*ClkInt

                self.Rf_TRampDo         =   (dCfg['Tp'] - dCfg['TRampUp'])
                dCfg['TRampDo']         =   (dCfg['Tp'] - dCfg['TRampUp'])

                if self.Rf_TRampDo/ClkInt < 10:
                    disp('Adf24Tx2Rx4: Set TRampDo to 10 cycles')
                    self.Rf_TRampDo     =   10*ClkInt
                    dCfg['TRampDo']     =   10*ClkInt

                # Configure ticks which are ignored in sampling
                Ticks                       =   floor((dCfg['TRampUp'] + dCfg['TRampDo'])/ClkInt)
                self.ADIFMCWCfg[7]      =   Ticks   - 256 - 1 - 7

                self.Dsp_SetAdiDefaultConf()

                if 'MimoEna' in dCfg:
                    if dCfg["MimoEna"] > 0:
                        print("Enable MIMO")
                        self.Dsp_SetMimo(1)


                self.RfAdf4159Ini(dCfg)

        return ErrCod

    # DOXYGEN ------------------------------------------------------
    #> @brief Reset frontend
    #>
    #> Reset frontend; Disables and enabled supply to reset frontend
    #>
    def     RfRst(self):
        self.BrdPwrDi()
        self.BrdPwrEna()

    # DOXYGEN ------------------------------------------------------
    #> @brief Initialize PLL with selected configuration
    #>
    #> Configures PLL
    #>
    #> @param[in]   Cfg: structure with PLL configuration
    #>      -   <span style="color: #ff9900;"> 'fStrt': </span> Start frequency in Hz
    #>      -   <span style="color: #ff9900;"> 'fStrt': </span> Stop frequency in Hz
    #>      -   <span style="color: #ff9900;"> 'TRampUp': </span> Upchirp duration in s
    #>
    #> %> @note Function is obsolete in class version >= 1.0.0: use function Adf_Pll.SetCfg() and Adf_Pll.Ini()
    def     RfAdf4159Ini(self, Cfg):
        self.Adf_Pll.SetCfg(Cfg);
        self.Adf_Pll.Ini();
