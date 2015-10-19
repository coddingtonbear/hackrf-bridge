#!/usr/bin/env python2
##################################################
# GNU Radio Python Flow Graph
# Title: Top Block
# Generated: Sun Oct 18 22:26:35 2015
##################################################

if __name__ == '__main__':
    import ctypes
    import sys
    if sys.platform.startswith('linux'):
        try:
            x11 = ctypes.cdll.LoadLibrary('libX11.so')
            x11.XInitThreads()
        except:
            print "Warning: failed to XInitThreads()"

from PyQt4 import Qt
from gnuradio import analog
from gnuradio import audio
from gnuradio import blocks
from gnuradio import eng_notation
from gnuradio import filter
from gnuradio import gr
from gnuradio import qtgui
from gnuradio.eng_option import eng_option
from gnuradio.filter import firdes
from gnuradio.qtgui import Range, RangeWidget
from optparse import OptionParser
import osmosdr
import sip
import sys
import time

from distutils.version import StrictVersion
class top_block(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "Top Block")
        Qt.QWidget.__init__(self)
        self.setWindowTitle("Top Block")
        try:
             self.setWindowIcon(Qt.QIcon.fromTheme('gnuradio-grc'))
        except:
             pass
        self.top_scroll_layout = Qt.QVBoxLayout()
        self.setLayout(self.top_scroll_layout)
        self.top_scroll = Qt.QScrollArea()
        self.top_scroll.setFrameStyle(Qt.QFrame.NoFrame)
        self.top_scroll_layout.addWidget(self.top_scroll)
        self.top_scroll.setWidgetResizable(True)
        self.top_widget = Qt.QWidget()
        self.top_scroll.setWidget(self.top_widget)
        self.top_layout = Qt.QVBoxLayout(self.top_widget)
        self.top_grid_layout = Qt.QGridLayout()
        self.top_layout.addLayout(self.top_grid_layout)

        self.settings = Qt.QSettings("GNU Radio", "top_block")
        self.restoreGeometry(self.settings.value("geometry").toByteArray())


        ##################################################
        # Variables
        ##################################################
        self.audio_rate = audio_rate = int(48e3)
        self.rtl_rate = rtl_rate = int(2.4e6)
        self.out_pre_transmission_audio_level = out_pre_transmission_audio_level = 1
        self.out_intermediary_rate = out_intermediary_rate = audio_rate*4
        self.out_frequency_offset = out_frequency_offset = -35e3
        self.out_frequency = out_frequency = 145.521e6
        self.out_fm_sensitivity = out_fm_sensitivity = 800e-3
        self.out_audio_level = out_audio_level = 1
        self.in_frequency_offset = in_frequency_offset = 0
        self.in_frequency = in_frequency = 145.521e6
        self.in_final_gain = in_final_gain = 4
        self.hackrf_rf_gain = hackrf_rf_gain = 0
        self.hackrf_rate = hackrf_rate = 2e6
        self.hackrf_if_gain = hackrf_if_gain = 10
        self.hackrf_bb_gain = hackrf_bb_gain = 10
        self.dstar_bandwidth = dstar_bandwidth = 6.5e3
        self.center_freq = center_freq = 429000000

        ##################################################
        # Blocks
        ##################################################
        self._out_pre_transmission_audio_level_range = Range(100e-3, 100, 100e-3, 1, 200)
        self._out_pre_transmission_audio_level_win = RangeWidget(self._out_pre_transmission_audio_level_range, self.set_out_pre_transmission_audio_level, "Pre-Transmission Level", "counter_slider")
        self.top_layout.addWidget(self._out_pre_transmission_audio_level_win)
        self._out_audio_level_range = Range(0.1, 5, 0.1, 1, 200)
        self._out_audio_level_win = RangeWidget(self._out_audio_level_range, self.set_out_audio_level, "Audio Level", "counter_slider")
        self.top_layout.addWidget(self._out_audio_level_win)
        _hackrf_rf_gain_check_box = Qt.QCheckBox("RF Amplifier Enabled")
        self._hackrf_rf_gain_choices = {True: 14, False: 0}
        self._hackrf_rf_gain_choices_inv = dict((v,k) for k,v in self._hackrf_rf_gain_choices.iteritems())
        self._hackrf_rf_gain_callback = lambda i: Qt.QMetaObject.invokeMethod(_hackrf_rf_gain_check_box, "setChecked", Qt.Q_ARG("bool", self._hackrf_rf_gain_choices_inv[i]))
        self._hackrf_rf_gain_callback(self.hackrf_rf_gain)
        _hackrf_rf_gain_check_box.stateChanged.connect(lambda i: self.set_hackrf_rf_gain(self._hackrf_rf_gain_choices[bool(i)]))
        self.top_layout.addWidget(_hackrf_rf_gain_check_box)
        self._hackrf_if_gain_range = Range(0, 40, 1, 10, 200)
        self._hackrf_if_gain_win = RangeWidget(self._hackrf_if_gain_range, self.set_hackrf_if_gain, "IF Gain", "counter_slider")
        self.top_layout.addWidget(self._hackrf_if_gain_win)
        self._hackrf_bb_gain_range = Range(0, 62, 1, 10, 200)
        self._hackrf_bb_gain_win = RangeWidget(self._hackrf_bb_gain_range, self.set_hackrf_bb_gain, "BB Gain", "counter_slider")
        self.top_layout.addWidget(self._hackrf_bb_gain_win)
        self.rtlsdr_source_0 = osmosdr.source( args="numchan=" + str(1) + " " + "" )
        self.rtlsdr_source_0.set_sample_rate(rtl_rate)
        self.rtlsdr_source_0.set_center_freq(in_frequency+in_frequency_offset, 0)
        self.rtlsdr_source_0.set_freq_corr(77, 0)
        self.rtlsdr_source_0.set_dc_offset_mode(0, 0)
        self.rtlsdr_source_0.set_iq_balance_mode(0, 0)
        self.rtlsdr_source_0.set_gain_mode(False, 0)
        self.rtlsdr_source_0.set_gain(10, 0)
        self.rtlsdr_source_0.set_if_gain(20, 0)
        self.rtlsdr_source_0.set_bb_gain(20, 0)
        self.rtlsdr_source_0.set_antenna("", 0)
        self.rtlsdr_source_0.set_bandwidth(0, 0)
          
        self.rational_resampler_xxx_3 = filter.rational_resampler_ccc(
                interpolation=int(hackrf_rate),
                decimation=out_intermediary_rate,
                taps=None,
                fractional_bw=None,
        )
        self.rational_resampler_xxx_1 = filter.rational_resampler_ccc(
                interpolation=audio_rate*5,
                decimation=rtl_rate,
                taps=None,
                fractional_bw=None,
        )
        self.qtgui_sink_x_1 = qtgui.sink_f(
        	1024, #fftsize
        	firdes.WIN_BLACKMAN_hARRIS, #wintype
        	0, #fc
        	out_intermediary_rate, #bw
        	"", #name
        	True, #plotfreq
        	True, #plotwaterfall
        	True, #plottime
        	True, #plotconst
        )
        self.qtgui_sink_x_1.set_update_time(1.0/10)
        self._qtgui_sink_x_1_win = sip.wrapinstance(self.qtgui_sink_x_1.pyqwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_sink_x_1_win)
        
        self.qtgui_sink_x_1.enable_rf_freq(False)
        
        
          
        self.qtgui_sink_x_0_0 = qtgui.sink_f(
        	1024, #fftsize
        	firdes.WIN_BLACKMAN_hARRIS, #wintype
        	0, #fc
        	audio_rate, #bw
        	"Received", #name
        	True, #plotfreq
        	True, #plotwaterfall
        	True, #plottime
        	True, #plotconst
        )
        self.qtgui_sink_x_0_0.set_update_time(1.0/10)
        self._qtgui_sink_x_0_0_win = sip.wrapinstance(self.qtgui_sink_x_0_0.pyqwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_sink_x_0_0_win)
        
        self.qtgui_sink_x_0_0.enable_rf_freq(False)
        
        
          
        self._out_fm_sensitivity_range = Range(10e-3, 10, 10e-3, 800e-3, 200)
        self._out_fm_sensitivity_win = RangeWidget(self._out_fm_sensitivity_range, self.set_out_fm_sensitivity, "FM Sensitivity", "counter_slider")
        self.top_layout.addWidget(self._out_fm_sensitivity_win)
        self.osmosdr_sink_0 = osmosdr.sink( args="numchan=" + str(1) + " " + "" )
        self.osmosdr_sink_0.set_sample_rate(hackrf_rate)
        self.osmosdr_sink_0.set_center_freq(out_frequency-out_frequency_offset, 0)
        self.osmosdr_sink_0.set_freq_corr(4, 0)
        self.osmosdr_sink_0.set_gain(hackrf_rf_gain, 0)
        self.osmosdr_sink_0.set_if_gain(hackrf_if_gain, 0)
        self.osmosdr_sink_0.set_bb_gain(hackrf_bb_gain, 0)
        self.osmosdr_sink_0.set_antenna("", 0)
        self.osmosdr_sink_0.set_bandwidth(100e3, 0)
          
        self.low_pass_filter_1 = filter.fir_filter_ccf(1, firdes.low_pass(
        	1, audio_rate*5, dstar_bandwidth, 200, firdes.WIN_HAMMING, 6.76))
        self.low_pass_filter_0 = filter.fir_filter_fff(1, firdes.low_pass(
        	1, audio_rate, dstar_bandwidth*2, 200, firdes.WIN_KAISER, 6.76))
        self.freq_xlating_fft_filter_ccc_0 = filter.freq_xlating_fft_filter_ccc(1, (1, ), 0-out_frequency_offset, out_intermediary_rate)
        self.freq_xlating_fft_filter_ccc_0.set_nthreads(1)
        self.freq_xlating_fft_filter_ccc_0.declare_sample_delay(0)
        self.blocks_multiply_const_vxx_2 = blocks.multiply_const_vff((0-out_audio_level, ))
        self.blocks_multiply_const_vxx_1 = blocks.multiply_const_vff((0-in_final_gain, ))
        self.blocks_multiply_const_vxx_0 = blocks.multiply_const_vcc((out_pre_transmission_audio_level, ))
        self.audio_source_0 = audio.source(audio_rate, "Soundflower (64ch)", True)
        self.audio_sink_1 = audio.sink(audio_rate, "Soundflower (2ch)", False)
        self.analog_pwr_squelch_xx_0_0 = analog.pwr_squelch_cc(-60, 1, 1, False)
        self.analog_pwr_squelch_xx_0 = analog.pwr_squelch_ff(-80, 1, 1, True)
        self.analog_nbfm_tx_0 = analog.nbfm_tx(
        	audio_rate=int(audio_rate),
        	quad_rate=int(out_intermediary_rate),
        	tau=0,
        	max_dev=6.25e3*2,
        )
        self.analog_fm_demod_cf_0 = analog.fm_demod_cf(
        	channel_rate=audio_rate*5,
        	audio_decim=5,
        	deviation=dstar_bandwidth*2,
        	audio_pass=dstar_bandwidth,
        	audio_stop=dstar_bandwidth+1e3,
        	gain=1,
        	tau=0,
        )

        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_fm_demod_cf_0, 0), (self.blocks_multiply_const_vxx_1, 0))    
        self.connect((self.analog_nbfm_tx_0, 0), (self.blocks_multiply_const_vxx_0, 0))    
        self.connect((self.analog_pwr_squelch_xx_0, 0), (self.blocks_multiply_const_vxx_2, 0))    
        self.connect((self.analog_pwr_squelch_xx_0_0, 0), (self.analog_fm_demod_cf_0, 0))    
        self.connect((self.audio_source_0, 0), (self.analog_pwr_squelch_xx_0, 0))    
        self.connect((self.blocks_multiply_const_vxx_0, 0), (self.freq_xlating_fft_filter_ccc_0, 0))    
        self.connect((self.blocks_multiply_const_vxx_1, 0), (self.audio_sink_1, 0))    
        self.connect((self.blocks_multiply_const_vxx_1, 0), (self.qtgui_sink_x_0_0, 0))    
        self.connect((self.blocks_multiply_const_vxx_2, 0), (self.low_pass_filter_0, 0))    
        self.connect((self.freq_xlating_fft_filter_ccc_0, 0), (self.rational_resampler_xxx_3, 0))    
        self.connect((self.low_pass_filter_0, 0), (self.analog_nbfm_tx_0, 0))    
        self.connect((self.low_pass_filter_0, 0), (self.qtgui_sink_x_1, 0))    
        self.connect((self.low_pass_filter_1, 0), (self.analog_pwr_squelch_xx_0_0, 0))    
        self.connect((self.rational_resampler_xxx_1, 0), (self.low_pass_filter_1, 0))    
        self.connect((self.rational_resampler_xxx_3, 0), (self.osmosdr_sink_0, 0))    
        self.connect((self.rtlsdr_source_0, 0), (self.rational_resampler_xxx_1, 0))    

    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "top_block")
        self.settings.setValue("geometry", self.saveGeometry())
        event.accept()

    def get_audio_rate(self):
        return self.audio_rate

    def set_audio_rate(self, audio_rate):
        self.audio_rate = audio_rate
        self.set_out_intermediary_rate(self.audio_rate*4)
        self.low_pass_filter_0.set_taps(firdes.low_pass(1, self.audio_rate, self.dstar_bandwidth*2, 200, firdes.WIN_KAISER, 6.76))
        self.low_pass_filter_1.set_taps(firdes.low_pass(1, self.audio_rate*5, self.dstar_bandwidth, 200, firdes.WIN_HAMMING, 6.76))
        self.qtgui_sink_x_0_0.set_frequency_range(0, self.audio_rate)

    def get_rtl_rate(self):
        return self.rtl_rate

    def set_rtl_rate(self, rtl_rate):
        self.rtl_rate = rtl_rate
        self.rtlsdr_source_0.set_sample_rate(self.rtl_rate)

    def get_out_pre_transmission_audio_level(self):
        return self.out_pre_transmission_audio_level

    def set_out_pre_transmission_audio_level(self, out_pre_transmission_audio_level):
        self.out_pre_transmission_audio_level = out_pre_transmission_audio_level
        self.blocks_multiply_const_vxx_0.set_k((self.out_pre_transmission_audio_level, ))

    def get_out_intermediary_rate(self):
        return self.out_intermediary_rate

    def set_out_intermediary_rate(self, out_intermediary_rate):
        self.out_intermediary_rate = out_intermediary_rate
        self.qtgui_sink_x_1.set_frequency_range(0, self.out_intermediary_rate)

    def get_out_frequency_offset(self):
        return self.out_frequency_offset

    def set_out_frequency_offset(self, out_frequency_offset):
        self.out_frequency_offset = out_frequency_offset
        self.freq_xlating_fft_filter_ccc_0.set_center_freq(0-self.out_frequency_offset)
        self.osmosdr_sink_0.set_center_freq(self.out_frequency-self.out_frequency_offset, 0)

    def get_out_frequency(self):
        return self.out_frequency

    def set_out_frequency(self, out_frequency):
        self.out_frequency = out_frequency
        self.osmosdr_sink_0.set_center_freq(self.out_frequency-self.out_frequency_offset, 0)

    def get_out_fm_sensitivity(self):
        return self.out_fm_sensitivity

    def set_out_fm_sensitivity(self, out_fm_sensitivity):
        self.out_fm_sensitivity = out_fm_sensitivity

    def get_out_audio_level(self):
        return self.out_audio_level

    def set_out_audio_level(self, out_audio_level):
        self.out_audio_level = out_audio_level
        self.blocks_multiply_const_vxx_2.set_k((0-self.out_audio_level, ))

    def get_in_frequency_offset(self):
        return self.in_frequency_offset

    def set_in_frequency_offset(self, in_frequency_offset):
        self.in_frequency_offset = in_frequency_offset
        self.rtlsdr_source_0.set_center_freq(self.in_frequency+self.in_frequency_offset, 0)

    def get_in_frequency(self):
        return self.in_frequency

    def set_in_frequency(self, in_frequency):
        self.in_frequency = in_frequency
        self.rtlsdr_source_0.set_center_freq(self.in_frequency+self.in_frequency_offset, 0)

    def get_in_final_gain(self):
        return self.in_final_gain

    def set_in_final_gain(self, in_final_gain):
        self.in_final_gain = in_final_gain
        self.blocks_multiply_const_vxx_1.set_k((0-self.in_final_gain, ))

    def get_hackrf_rf_gain(self):
        return self.hackrf_rf_gain

    def set_hackrf_rf_gain(self, hackrf_rf_gain):
        self.hackrf_rf_gain = hackrf_rf_gain
        self._hackrf_rf_gain_callback(self.hackrf_rf_gain)
        self.osmosdr_sink_0.set_gain(self.hackrf_rf_gain, 0)

    def get_hackrf_rate(self):
        return self.hackrf_rate

    def set_hackrf_rate(self, hackrf_rate):
        self.hackrf_rate = hackrf_rate
        self.osmosdr_sink_0.set_sample_rate(self.hackrf_rate)

    def get_hackrf_if_gain(self):
        return self.hackrf_if_gain

    def set_hackrf_if_gain(self, hackrf_if_gain):
        self.hackrf_if_gain = hackrf_if_gain
        self.osmosdr_sink_0.set_if_gain(self.hackrf_if_gain, 0)

    def get_hackrf_bb_gain(self):
        return self.hackrf_bb_gain

    def set_hackrf_bb_gain(self, hackrf_bb_gain):
        self.hackrf_bb_gain = hackrf_bb_gain
        self.osmosdr_sink_0.set_bb_gain(self.hackrf_bb_gain, 0)

    def get_dstar_bandwidth(self):
        return self.dstar_bandwidth

    def set_dstar_bandwidth(self, dstar_bandwidth):
        self.dstar_bandwidth = dstar_bandwidth
        self.low_pass_filter_0.set_taps(firdes.low_pass(1, self.audio_rate, self.dstar_bandwidth*2, 200, firdes.WIN_KAISER, 6.76))
        self.low_pass_filter_1.set_taps(firdes.low_pass(1, self.audio_rate*5, self.dstar_bandwidth, 200, firdes.WIN_HAMMING, 6.76))

    def get_center_freq(self):
        return self.center_freq

    def set_center_freq(self, center_freq):
        self.center_freq = center_freq


if __name__ == '__main__':
    parser = OptionParser(option_class=eng_option, usage="%prog: [options]")
    (options, args) = parser.parse_args()
    if(StrictVersion(Qt.qVersion()) >= StrictVersion("4.5.0")):
        Qt.QApplication.setGraphicsSystem(gr.prefs().get_string('qtgui','style','raster'))
    qapp = Qt.QApplication(sys.argv)
    tb = top_block()
    tb.start()
    tb.show()
    def quitting():
        tb.stop()
        tb.wait()
    qapp.connect(qapp, Qt.SIGNAL("aboutToQuit()"), quitting)
    qapp.exec_()
    tb = None #to clean up Qt widgets
