using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;

public class DisplayFPS : MonoBehaviour
{
    public bool displayFPS;
    string fpsText;
    float deltaTime = 0.0f;
    ListItem fpsItem;
    float msec;
    float fps;

    // Start is called before the first frame update
    void Start()
    {
        displayFPS = true;
        fpsItem = new ListItem(0);
        fpsItem.SetData("INFINITE FPS");
        ConsoleHandler.Instance.AddItemToConsole(fpsItem);
    }

    // Update is called once per frame
    void Update()
    {
        deltaTime += (Time.unscaledDeltaTime - deltaTime) * 0.1f;
        if (displayFPS)
        {
            float msec = deltaTime * 1000.0f;
            float fps = 1.0f / deltaTime;
            fpsText = ((int)fps).ToString() + " FPS";
            fpsItem.SetData(fpsText);
        }
        else
            fpsItem.SetData("");
    }
    
    public void ToggleFPSVisibility(bool setValue)
    {
        displayFPS = setValue;
    }
}