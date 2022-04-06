using System;
using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;
using uPLibrary.Networking.M2Mqtt;
using uPLibrary.Networking.M2Mqtt.Messages;
using M2MqttUnity;

public class Connection : MonoBehaviour {

    public InputField BrokerUrl;
    public InputField Username;
    public InputField Password;
    public string topic_to_subscribe = "#";

    public string brokerurl = "";
    public string username = "";
    public string password = "";


    private void Start() {

        // DontDestroyOnLoad(this);
        Debug.Log("LogIn");
        // BrokerUrl.text = "mqttserver.tk";
        // Username.text = "bkiot";
        // Password.text = "12345678";
        // BrokerUrl.text = "test.mosquitto.org";
        // Username.text = "rw";
        // Password.text = "readwrite";
        BrokerUrl.text = "test.mosquitto.org";
        Username.text = "wildcard";
        Password.text = "";

        brokerurl += BrokerUrl.text;
        username += Username.text;
        password += Password.text;
        DontDestroyOnLoad(this);
    }
}

