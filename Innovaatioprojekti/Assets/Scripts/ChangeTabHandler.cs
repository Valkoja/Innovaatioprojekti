using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;

public class ChangeTabHandler : MonoBehaviour
{

    public GameObject generalPanel;
    public GameObject renderPanel;

    //public Button generalButton;
    //public Button renderButton;

    public Image generalImage;
    public Image renderImage;

    bool generalPanelVisibility;
    bool renderPanelVisibility;

    //ColorBlock activeButtonColorBlock;
    //ColorBlock inactiveButtonColorBlock;

    Color32 activeButtonColor; // 137x3 + 34
    Color32 inactiveButtonColor; // 255x3 + 34

    // Start is called before the first frame update
    void Start()
    {
        generalPanelVisibility = true;
        renderPanelVisibility = false;
        activeButtonColor = new Color32(0x89, 0x89, 0x89, 0x22);
        inactiveButtonColor = new Color32(0xFF, 0xFF, 0xFF, 0x22);
        generalImage.color = activeButtonColor;
        renderImage.color = inactiveButtonColor;
        //activeButtonColorBlock = generalButton.colors;
        //inactiveButtonColorBlock = renderButton.colors;
        //activeButtonColorBlock.normalColor = activeButtonColor;
        //inactiveButtonColorBlock.normalColor = inactiveButtonColor;
        generalPanel.SetActive(generalPanelVisibility);
        renderPanel.SetActive(renderPanelVisibility);
    }

    // Update is called once per frame
    void Update()
    {
        
    }

    public void SetCurrentPanelToGeneral()
    {
        generalPanelVisibility = true;
        renderPanelVisibility = false;
        generalPanel.SetActive(generalPanelVisibility);
        renderPanel.SetActive(renderPanelVisibility);
        generalImage.color = activeButtonColor;
        renderImage.color = inactiveButtonColor;
        //generalButton.colors = activeButtonColorBlock;
        //renderButton.colors = inactiveButtonColorBlock;
    }

    public void SetCurrentPanelToRender()
    {
        renderPanelVisibility = true;
        generalPanelVisibility = false;
        renderPanel.SetActive(renderPanelVisibility);
        generalPanel.SetActive(generalPanelVisibility);
        generalImage.color = inactiveButtonColor;
        renderImage.color = activeButtonColor;
        //generalButton.colors = inactiveButtonColorBlock;
        //renderButton.colors = activeButtonColorBlock;
    }
}
