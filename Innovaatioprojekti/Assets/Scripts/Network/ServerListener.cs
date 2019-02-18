using System;
using System.Net;
using System.Net.Sockets;
using System.Text;
using UnityEngine;

public class ServerListener : MonoBehaviour
{
    public string serverAddress = "";
    private UdpClient client = null;
    private const int port = 9000;
    private IPEndPoint broadcastAddress = new IPEndPoint(IPAddress.Any, port);

    void Start()
    {
        try {
            Debug.Log("Start listener..");
            this.client = new UdpClient();
            this.client.Client.SetSocketOption(SocketOptionLevel.Socket, SocketOptionName.ReuseAddress, true);
            this.client.ExclusiveAddressUse = false;
            this.client.Client.Bind(this.broadcastAddress);
            this.client.BeginReceive(new AsyncCallback(this.ReceiveCallback), null);
        }
        catch(Exception e)
        {
            Debug.Log("Something went wrong");
            Debug.Log(e);
        }  
    }

    void Update()
    {
        
    }

    void OnDestroy()
    {
        client.Close();
        Debug.Log("Client disposed.");
    }

    void ReceiveCallback(IAsyncResult ar)
    {
        byte[] receiveBytes = client.EndReceive(ar, ref broadcastAddress);
        string receiveString = Encoding.ASCII.GetString(receiveBytes);
        Debug.Log("Message received");
        Debug.Log(receiveString);
        this.serverAddress = receiveString;
    }
}
