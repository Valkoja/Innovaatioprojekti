using System;
using System.Collections;
using System.Collections.Generic;
using System.Text.RegularExpressions;
using UnityEngine;
using UnityEngine.UI;

public class IPSetHandler : MonoBehaviour
{
    const string IPv4 = @"^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$";
    public Text inputFieldText;
    public Text currentHostIPText;
    string inputText = "";

    // Start is called before the first frame update
    void Start()
    {
        
    }

    // Update is called once per frame
    void Update()
    {
        
    }

    async public void OnPressConfirm()
    {
        inputText = inputFieldText.text;
        if (IsInputIPCorrect(inputText))
        {
            currentHostIPText.text = inputText;
            ConsoleHandler.Instance.AddItemToConsole(new ListItem("Connecting to "+inputText+"...",1,"R"));
            await Network.ConnectToServer(inputText);
        }
        else {
            ConsoleHandler.Instance.AddItemToConsole(new ListItem("Invalid address",1,"R"));
        }
    }

    public void OnPressCancel()
    {
        // tanne jtn?
    }

    bool IsInputIPCorrect(string input)
    {
        try {
            return Regex.IsMatch(input, IPv4, RegexOptions.IgnoreCase, TimeSpan.FromMilliseconds(250));
        }
        catch (RegexMatchTimeoutException)
        {
            return false;
        }
    }
}
