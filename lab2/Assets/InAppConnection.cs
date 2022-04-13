using System;
using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;
using uPLibrary.Networking.M2Mqtt;
using uPLibrary.Networking.M2Mqtt.Messages;
using M2MqttUnity;

public class InAppConnection : M2MqttUnityClient {
    public Text datetime;
    private string topic_to_subscribe = "/bkiot/1852247/status";
    public Text temp;
    public Image tempBar;
    public Text humid;
    public Image humidBar;
    public Toggle toggleLED;
    public Toggle togglePump;

    // Start is called before the first frame update
    protected override void Start() {
        ConnectServer();
        base.Start();
        // led.enabled = true;
        // isLedOn = true;
    }

    protected override void Update () {
        base.Update();
        datetime.text = DateTime.Now.ToString();
        // GetMessage();
        // if (Input.GetKeyDown ("i")) {
        //     if (isLedOn == true) {
        //         led.enabled = false;
        //         isLedOn = false;
        //     } else {
        //         led.enabled = true;
        //         isLedOn = true;
        //     }
        // }
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
            Debug.Log("Subscribe now!");
            client.Subscribe(new string[] { "/bkiot/1852247/status" }, new byte[] { MqttMsgBase.QOS_LEVEL_EXACTLY_ONCE });
        }
    }

    public void Unsubscribe() {
        client.Unsubscribe(new string[] { "/bkiot/1852247/status" });
    }

    public void PublishLED() {
        PublishMessage message = new PublishMessage();
        message.device = "LED";
        message.status = toggleLED.isOn ? "ON" : "OFF";
        string json = JsonUtility.ToJson(message);
        client.Publish("/bkiot/1852247/led", System.Text.Encoding.UTF8.GetBytes(json), MqttMsgBase.QOS_LEVEL_EXACTLY_ONCE, false);
        Debug.Log("Test message published: " + json);
    }

    public void PublishPump() {
        PublishMessage message = new PublishMessage();
        message.device = "PUMP";
        message.status = togglePump.isOn ? "ON" : "OFF";
        string json = JsonUtility.ToJson(message);
        client.Publish("/bkiot/1852247/pump", System.Text.Encoding.UTF8.GetBytes(json), MqttMsgBase.QOS_LEVEL_EXACTLY_ONCE, false);
        Debug.Log("Test message published: " + json);
    }

    protected override void DecodeMessage(string topic, byte[] message) {
        // Debug.Log(message.temperature);
        try {
            string str = System.Text.Encoding.UTF8.GetString(message);
            Debug.Log("Received: " + str);
            Message json = JsonUtility.FromJson<Message>(str);

            float tempValue = (float)Math.Round(json.temperature, 2);
            temp.text = "Temperature: " + tempValue.ToString() + "°C";
            tempBar.fillAmount = tempValue / 100;

            float humidValue = (float)Math.Round(json.humidity, 2);
            humid.text = "Humidity: " + humidValue.ToString();
            humidBar.fillAmount = humidValue / 100;
            
            // StoreMessage(msg);
            } catch (ArgumentException) {}
    }

    private void AddUiMessage(string msg) {
        print(msg);
    }
    
}

[Serializable]
public class Message {
    public float temperature;
    public float humidity;
}

[Serializable]
public class PublishMessage {
    public string device;
    public string status;
}