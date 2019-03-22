using System;
using UnityEngine;

[System.Serializable]
public class XSiteDataConfirmationMessage
{
    public string type = "CONFIRM";
    public int id;
    public string timestamp;

    public static XSiteDataConfirmationMessage FromDataMessage(XSiteDataMessage message)
    {
        return new XSiteDataConfirmationMessage {id = message.id, timestamp = message.timestamp};
    }
}