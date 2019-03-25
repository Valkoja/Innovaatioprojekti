using System;
using UnityEngine;

[System.Serializable]
public class XSiteDataHelloMessage
{
    public string type = "HELLO";
    public string library = "Unity";
    public string platform = SystemInfo.operatingSystem;
    public string version = "0.1-alpha";
}