#!/usr/bin/env python
# -*- coding: utf-8 -*-
# pylint: disable=W0613, C0116
# type: ignore[union-attr]
# This program is dedicated to the public domain under the CC0 license.

"""
Simple Bot to send timed Telegram messages.
This Bot uses the Updater class to handle the bot and the JobQueue to send
timed messages.
First, a few handler functions are defined. Then, those functions are passed to
the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.
Usage:
Basic Alarm Bot example, sends a message after a set time.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""
import logging

from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext

import RPi.GPIO as GPIO
import time
import spidev

from phue import Bridge
import datetime

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)


# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.

def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('/help를 통해 사용법을 확인하세요!')

def water(update: Update, context: CallbackContext) -> None:
    HUM_THRESHOLD=20
    HUM_MAX=0

    spi=spidev.SpiDev()
    spi.open(0,0)
    spi.max_speed_hz=500000

    def read_spi_adc(adcChannel):
        adcValue=0
        buff=spi.xfer2([1,(8+adcChannel)<<4,0])
        adcValue=((buff[1]&3)<<8)+buff[2]
        return adcValue

    def map(value,min_adc,max_adc,min_hum,max_hum):
        adc_range=max_adc-min_adc
        hum_range=max_hum-min_hum
        scale_factor=float(adc_range)/float(hum_range)
        return min_hum+((value-min_adc)/scale_factor)

    try:
        adcChannel=0
        while True:
            adcValue=read_spi_adc(adcChannel)
            hum=100-int(map(adcValue,HUM_MAX,1023,0,100))
            if hum<HUM_THRESHOLD:
                print('Water Value : {0}'.format(hum))
                update.message.reply_text('WaterLack!!!!')
            else:
                print('Water Value : {0}'.format(hum))
                update.message.reply_text('수분이 충분합니다 :)')
                break
            time.sleep(3)
    finally:
        spi.close()

def led(update: Update, context: CallbackContext) -> None:
    start_time = context.args[0]
    duration_sec = int(context.args[1])
    light_intensity = int(context.args[2])
    color = context.args[3]
    
    if color == '파랑':
        x_y = [0.15,0.06]
    elif color == '빨강':
        x_y = [0.6,0.3]

    # 입력받은 지속시간 값을 통해 예약시간으로부터 LED 꺼지는 시간을 처리해주는 코드 
    st_before = start_time[0:10]
    st_after = start_time[11:]
    
    b_a_str = st_before + " " + st_after
    b_a_date = datetime.datetime.strptime(b_a_str,'%Y-%m-%d %H:%M:%S')

    b_a_add = b_a_date + datetime.timedelta(seconds=duration_sec)
    b_a_add_str = b_a_add.strftime('%Y-%m-%d %H:%M:%S')
    b_a_add_str_b = b_a_add_str[0:10]
    b_a_add_str_a = b_a_add_str[11:]

    finish_time = b_a_add_str_b + 'T' + b_a_add_str_a

    b = Bridge('192.168.0.12')
    data_on = {'on' : True, 'bri' : light_intensity, 'xy' : x_y}
    b.create_schedule('Led on', start_time , 1, data_on,'Plant Led On')

    data_off = {'on' : False}
    b.create_schedule('Led off', finish_time, 1, data_off, 'Plant Led Off')
    
    update.message.reply_text('예약이 완료되었습니다!')

def h_t_u(update: Update, context:CallbackContext) -> None:
    update.message.reply_text('# 토양 수분 부족 알림'+'\n'+'형식 : /water')
    #update.message.reply_text('---------------------------')
    update.message.reply_text('# LED 시간 예약 및 빛/색 조절'+'\n'+'형식 : /led 날짜T시간 지속시간 빛세기 색'+'\n'+'\n'+'날짜 : @@@@-@@-@@ 형식'+'\n'+'시간 : @@:@@:@@ 형식'+'\n'+'지속시간 : 10 = 10초'+'\n'+'빛세기 : 0~254 사이의 수'+'\n'+'색 : 파랑-식물 광합성 / 빨강- 식물 생장'+'\n'+'\n'+'예) /led 2020-12-16T17:00:00 10 254 파랑')

def main():
    """Run bot."""
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater("MY TOKEN", use_context=True)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # on different commands - answer in Telegram
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("water", water))
    dispatcher.add_handler(CommandHandler("led", led, pass_args=True))
    dispatcher.add_handler(CommandHandler("help", h_t_u))

    # Start the Bot
    updater.start_polling()

    # Block until you press Ctrl-C or the process receives SIGINT, SIGTERM or
    # SIGABRT. This should be used most of the time, since start_polling() is
    # non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
