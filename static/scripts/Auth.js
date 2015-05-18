
Ext.onReady(function(){
    Ext.define("My.scripts.Auth", {
        loginDlg: 'Unknown',
        constructor: function(title, url, operation){
            f = new Ext.FormPanel({
                labelWidth: 100,
                url: url,
                frame: true,
                defaults: {width: 100},
                items: [{xtype: 'textfield',
                    fieldLabel: 'User name',
                    name: 'username',
                    vtype: 'alpha',
                    allowBlank: false},
                    {xtype: 'textfield',
                    inputType: 'password',
                    fieldLabel: 'Password',
                    name: 'password',
                    allowBlank: false},
                    {
                        xtype : 'hidden',  //should use the more standard hiddenfield
                        name  : 'operation',
                        value : operation,
                    }

                ],
                buttons: [{
                    text: 'OK',
                    minWidth: 75,
                    handler: function() {
                        f.getForm().submit({
                            success: function(form, action){
                                //Ext.Msg.alert('Success', 'It worked');
                                loginDlg.close();
                            },
                            failure: function(form, action){
                                Ext.Msg.alert('Warning', action.result.errormsg);
                            }
                        });
                    }
                },{
                    text: 'Cancel',
                    minWidth: 75,
                    handler: function() {
                        loginDlg.close();
                    }
                }]
            });
            loginDlg = new Ext.Window({
                height: 140,
                width: 300,
                closable: true,
                closeAction : 'hide',
                modal: true,
                title: title,
                layout: 'fit',
                items: f
            });
            this.loginDlg = loginDlg;
            //this.show();
            //this.close();
        },

        show: function() {
            this.loginDlg.show();
        }
    });
});