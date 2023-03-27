"""Test loading XAML in IronPython."""
#pylint: disable=import-error,invalid-name,broad-except,superfluous-parens
import sys
import urllib2
import json
from time import sleep

import threading
import requests

import os.path as op
from pyrevit import EXEC_PARAMS
import os
#if need proxy
proxy_address = 'http://127.0.0.1:7890'
os.environ['HTTP_PROXY'] = proxy_address
os.environ['HTTPS_PROXY'] = proxy_address

from pyrevit import framework
from pyrevit import coreutils
from pyrevit import revit, DB
from pyrevit import forms
from pyrevit import script
import System.Net
import System.IO
from System import Threading

logger = script.get_logger()
output = script.get_output()
CERROR="#d71345A2"
CINFO="#f6f5ec"
CWARN="#faa755"
CSUCCESS="#1d953fA2"

class ViewModel(forms.Reactive):
    def __init__(self):
        self.user_input_message=""
        self.token=""
        self._conversations=[]
    
class UI(forms.WPFWindow, forms.Reactive):
    def __init__(self):
        self.vm = ViewModel()

    def setup(self):
        self.vm.user_input_message=self.UserInputTextBox.Text
        self.vm.token=self.TokenInput.Text
        self.set_image_source(self.chatLogo, 'icon.png')
        self.AddMessage("agent","Hello,welcome to use revit-chatGPT!")
        

    def SubmitButton_Click(self,sender, args):
        user_input=self.vm.user_input_message
        if user_input:
            self.AddMessage(role="User",message=user_input)
            #process request
            self.ProcessUserInput()
        else:
            self.AddMessage(role="agent",message="no request")

    def GetInputToken(self,sender,args):
        self.vm.token=self.TokenInput.Text
        if self.vm.token.strip()=="":
            self.AddMessage("agent","got Token!")
       
    def GetUserInput(self,sender,args):
        self.vm.user_input_message=self.UserInputTextBox.Text.strip()

    def ProcessUserInput(self):
        text = self.vm.user_input_message
        if not text:
            return

        if self.vm.token.strip()=="":
            self.Dispatcher.Invoke(lambda: self.AddMessage("agent","please input api token!"))

        if text!="":
            self.Dispatcher.Invoke(lambda: self.AddMessage("agent", "ok,copied!"))
        #create a new thread
        t = threading.Thread(target=self.CallChatGPT, args=(text,self.vm.token))
        t.start()
        
    def CallChatGPT(self,input_text,token):
        openai_key = token
        url = "https://api.openai.com/v1/completions"
        request = System.Net.WebRequest.Create(url)
        request.Method = "POST"
        request.Headers.Add("Authorization", "Bearer " + openai_key)
        request.ContentType = "application/json"
        #The token count of your prompt plus maxtokens cannot exceed the model's context length. Most models have a context length of 2048 tokens (except for the newest models, which support 4096).
        #to use more detail instruction,reffer to visual-chatGPT 
	  data = {
            "model": "text-davinci-003",
            "prompt": input_text,
            "temperature": 0.7,
            "max_tokens": 2048
        }
        json_data = json.dumps(data)
        bytes_data = framework.Encoding.ASCII.GetBytes(json_data)
        request.ContentLength = bytes_data.Length
        stream = request.GetRequestStream()
        stream.Write(bytes_data, 0, bytes_data.Length)
        stream.Close()
        try:
            response = request.GetResponse()
        except System.Net.WebException as e:
            response = e.Response
        if response:
            if response.StatusCode ==System.Net.HttpStatusCode.OK:
                response_stream = response.GetResponseStream()
                reader =  System.IO.StreamReader(response_stream)
                response_data = reader.ReadToEnd()
                self.Dispatcher.Invoke(lambda: self.DisplayChatResponseResult(response_data))
            elif response.StatusCode == System.Net.HttpStatusCode.Unauthorized:
                self.Dispatcher.Invoke(lambda:self.AddMessage("agent","OpenAI authorization failed with the provided API key."))
            elif response.StatusCode == System.Net.HttpStatusCode.InternalServerError:
                self.Dispatcher.Invoke(lambda:self.AddMessage("agent","OpenAI internal server error."))
            else:
                self.Dispatcher.Invoke(lambda:self.AddMessage("agent","Unexpected OpenAI response status code: {}".format(response.StatusCode)))
            response.Close()
        
        
    def DisplayChatResponseResult(self, response_data):
        '''display chatResponse'''
        if response_data:
            result=json.loads(response_data,encoding="utf-8")
            # if result["error"] is not None:
            #     error_message=result["error"]["message"]
            #     self.AddMessage(role="chatGPT",message=error_message,color=CERROR)
            #     self.AddMessage(role="agent",message="pay attention to error!")
            
            output_text = result["choices"][0]["text"]
            self.AddMessage(role="chatGPT",message=output_text,color=CSUCCESS)
            #do revit work ,let it auto work ,refference visual-chatgpt
            self.DoRevitWork(actions=[])
                    
    def AddMessage(self,role,message,color=CINFO):
        '''add message of different role'''
        message_block=framework.Controls.TextBlock()
        message_block.Width = 500
        message_block.TextWrapping = framework.Windows.TextWrapping.Wrap
        message_block.Text=role+":\n"+message
        message_block.FontSize=16
        brush_color=framework.Windows.Media.ColorConverter.ConvertFromString(color)
        brush=framework.Windows.Media.SolidColorBrush(brush_color)
        message_block.Background=brush
        self.ConversationStackPanel.Children.Add(message_block)
    
    def DoRevitWork(self,actions):
        pass
    
# init ui
ui = script.load_ui(UI(), 'dialog.xaml')
# show modal or nonmodal
#ui.show_dialog()
#nonmodal
ui.show()
