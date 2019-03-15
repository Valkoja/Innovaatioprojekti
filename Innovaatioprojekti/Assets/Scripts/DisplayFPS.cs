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
        fpsItem = new ListItem(0,"L");
        fpsItem.SetData("0 FPS");
        ConsoleHandler.Instance.AddItemToConsole(fpsItem);
    }

    // Update is called once per frame
    void Update()
    {
        deltaTime += (Time.unscaledDeltaTime - deltaTime) * 0.1f;
        float msec = deltaTime * 1000.0f;
        float fps = 1.0f / deltaTime;
        fpsText = ((int)fps).ToString() + " FPS";
        fpsItem.SetData(fpsText);
    }
    
    public void ToggleFPSVisibility(bool setValue)
    {
        if (setValue)
        {
            fpsItem.SetAType(0);
        }
        else
        {
            fpsItem.SetAType(2);
        }
    }
}