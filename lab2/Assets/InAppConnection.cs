using System;
using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;
using uPLibrary.Networking.M2Mqtt;
using uPLibrary.Networking.M2Mqtt.Messages;
using M2MqttUnity;

public class InAppConnection : M2MqttUnityClient {


    private string topic_to_subscribe = "#";
    // private string topic_to_subscribe = "/bkiot/1852740/status";
    public Text msg_received_from_topic;

    // Start is called before the first frame update
    protected override void Start() {
        ConnectServer();
    }

    private void ConnectServer() {
        var connection = FindObjectOfType<Connection>();
        this.brokerAddress = connection.brokerurl;
        this.brokerPort = 1883;
        this.mqttUserName = connection.username;
        this.mqttPassword = connection.password;

        if (this.brokerAddress == "") {
            print("Please enter something");
            return;
        }
        this.Connect();
        Debug.Log("Connect Successfully");
    }


    public void GetMessage() {
        if (topic_to_subscribe != "") {
            client.Subscribe(new string[] { topic_to_subscribe }, new byte[] { MqttMsgBase.QOS_LEVEL_EXACTLY_ONCE });
        }
    }


    public void TestPublish() {
        client.Publish(topic_to_subscribe, System.Text.Encoding.UTF8.GetBytes("Test message"), MqttMsgBase.QOS_LEVEL_EXACTLY_ONCE, false);
        Debug.Log("Test message published");
        AddUiMessage("Test message published.");
    }

    protected override void DecodeMessage(string topic, byte[] message) {
        string msg = System.Text.Encoding.UTF8.GetString(message);
        msg_received_from_topic.text = msg;
        Debug.Log("Received: " + msg);
        // StoreMessage(msg);
    }

    private void AddUiMessage(string msg) {
        print(msg);
    }
    
}
