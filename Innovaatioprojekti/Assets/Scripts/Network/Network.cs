using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Net;
using System.Net.WebSockets;
using System.Text;
using System.Threading;
using System.Threading.Tasks;
using UnityEngine;

public class Network : MonoBehaviour
{
    static ClientWebSocket webSocket = new ClientWebSocket();
    private const int sendChunkSize = 256;
    private const int receiveChunkSize = 64;
    private const bool verbose = true;
    private static readonly TimeSpan delay = TimeSpan.FromMilliseconds(1000);
    private static string address;
    private static GameObject stateObject;
    const int maxConnectionAttempts = 5;
    private static int connectionAttempts = 0;
    
    private static ListItem latencyItem;
    private static ListItem tickrateItem;

    private void Start()
    {
        Debug.Log("Init network");
        stateObject = GameObject.Find("MachineState");
        latencyItem = new ListItem(0,"T");
        latencyItem.SetData("- ms");
        ConsoleHandler.Instance.AddItemToConsole(latencyItem);
        tickrateItem = new ListItem(0,"T");
        tickrateItem.SetData("- Hz");
        ConsoleHandler.Instance.AddItemToConsole(tickrateItem);
    }

    private void OnDestroy()
    {
        if (webSocket != null) {
            webSocket.Abort();
            webSocket.Dispose();
        }
        Debug.Log("WebSocket disposed.");
    }

    public static async Task ConnectToServer(string ip) {
        address = ip;
        ConsoleHandler.Instance.AddItemToConsole(new ListItem("Connecting...",1,"R"));
        webSocket = new ClientWebSocket();
        await Connect("ws://" + address + ":9000");
    }

    private static async Task Reconnect() {
        ConsoleHandler.Instance.AddItemToConsole(new ListItem("Lost connection, reconnecting in 5...",1,"R"));
        connectionAttempts += 1;
        await Task.Delay(TimeSpan.FromSeconds(5));
        await ConnectToServer(address);
    }

    public static async Task Connect(string uri)
    {
        try
        {
            await webSocket.ConnectAsync(new Uri(uri), CancellationToken.None);
            ConsoleHandler.Instance.AddItemToConsole(new ListItem($"Connected to {address}",1,"R"));
            connectionAttempts += 1;
            // await SendStringAsync("{ \"type\": \"HELLO\", \"info\": { \"library\": \"C#\", \"client\": \"unity\" }}");
            var hello = JsonUtility.ToJson(new XSiteDataHelloMessage());
            await SendStringAsync(hello);
            await Task.WhenAll(ReceiveState(webSocket));
        }
        catch (Exception ex)
        {
            Debug.Log($"Exception: {ex.Message}");
            Debug.Log(webSocket.State);
        }
        finally
        {
            if(webSocket != null) {
                if(webSocket.State != WebSocketState.Closed) {
                    // Do something???
                }
                if(webSocket.State == WebSocketState.Closed && address != null && connectionAttempts < maxConnectionAttempts) {
                    await Reconnect();
                }
            }
            else if(connectionAttempts == maxConnectionAttempts) {
                ConsoleHandler.Instance.AddItemToConsole(new ListItem("Host unavailable",1,"R"));
            }
        }
    }

    private static async Task ReceiveState(ClientWebSocket webSocket)
    {
        while (webSocket.State == WebSocketState.Open)
        {
            var result = await ReceiveStringAsync();
            var message = JsonUtility.FromJson<XSiteDataMessage>(result);
            if(stateObject) {
                stateObject.GetComponent<MachineState>().consumeMessage(message.state);
                latencyItem.SetData(((int)message.latency).ToString() + " ms");
                tickrateItem.SetData(((int)message.tickRate).ToString() + " Hz");
                if (message.id % 50 != 0) continue;
                var response = JsonUtility.ToJson(XSiteDataConfirmationMessage.FromDataMessage(message));
                await SendStringAsync(response);
            }
            else {
                Debug.Log("No state available");
            }
        }
        if(webSocket.State == WebSocketState.Closed) {
            await Reconnect();
        }
    }

    private static Task SendStringAsync(string data, CancellationToken ct = default(CancellationToken))
    {
        var buffer = Encoding.UTF8.GetBytes(data);
        var segment = new ArraySegment<byte>(buffer);
        return webSocket.SendAsync(segment, WebSocketMessageType.Text, true, ct);
    }

    private static async Task<string> ReceiveStringAsync(CancellationToken ct = default(CancellationToken))
    {
        var buffer = new ArraySegment<byte>(new byte[8192]);
        using (var ms = new MemoryStream())
        {
            WebSocketReceiveResult result;
            do
            {
                ct.ThrowIfCancellationRequested();

                result = await webSocket.ReceiveAsync(buffer, ct);
                ms.Write(buffer.Array, buffer.Offset, result.Count);
            }
            while (!result.EndOfMessage);

            ms.Seek(0, SeekOrigin.Begin);
            if (result.MessageType != WebSocketMessageType.Text)
            {
                return null;
            }

            // Encoding UTF8: https://tools.ietf.org/html/rfc6455#section-5.6
            using (var reader = new StreamReader(ms, Encoding.UTF8))
            {
                return await reader.ReadToEndAsync();
            }
        }
    }
}
