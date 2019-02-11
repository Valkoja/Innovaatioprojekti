using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;

public class IPSetHandler : MonoBehaviour
{
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

    public void OnPressConfirm()
    {
        inputText = inputFieldText.text;
        if (IsInputIPCorrect(inputText))
        {
            currentHostIPText.text = inputText;
            ConsoleHandler.Instance.AddItemToConsole(new ListItem("Connecting to "+inputText+"...",1));
        }
    }

    public void OnPressCancel()
    {
        // tanne jtn?
    }

    bool IsInputIPCorrect(string input)
    {
        if (input != "")
        {
            return true;
        }
        else return false;
    }
}
