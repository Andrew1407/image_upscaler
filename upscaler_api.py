import telebot
import numpy as np
from io import BytesIO
from PIL import Image

from image_upscaler import ImageUpscaler


class UpscalerApi:
  def __init__(self, bot: telebot.TeleBot, upscaler: ImageUpscaler):
    self.__bot: telebot.TeleBot = bot
    self.__upscaler: ImageUpscaler = upscaler
    self.__bot.message_handler(commands=['start'])(self.__send_start_message)
    self.__bot.message_handler(content_types=['photo'])(self.__upscale_passed_image)


  def launch(self):
    self.__bot.polling()


  def __send_start_message(self, message: telebot.types.Message):
    text = 'Hello, this is an image upscaler bot; send an image here to get its upsaled form.'
    self.__bot.reply_to(message, text)


  def __upscale_passed_image(self, message: telebot.types.Message):
    file_id = message.photo[-1].file_id
    file_info = self.__bot.get_file(file_id)
    file = self.__bot.download_file(file_info.file_path)
    img = np.array(Image.open(BytesIO(file)))
    f = self.__upscaler.increase_resolution(img)
    self.__bot.send_document(message.chat.id, f)