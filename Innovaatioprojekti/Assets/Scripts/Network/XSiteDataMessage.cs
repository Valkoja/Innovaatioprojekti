using System;
using UnityEngine;

[System.Serializable]
public class XSiteDataMessage
{
    public MachineStateMessage state;
    public int id;
    public string timestamp;
    public float latency;
    public int tickRate;

    public static XSiteDataMessage CreateFromJSON(string jsonString)
    {
        return JsonUtility.FromJson<XSiteDataMessage>(jsonString);
    }
}