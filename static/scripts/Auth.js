
Ext.onReady(function(){
    Ext.define("My.scripts.Auth", {
        loggedInVar: false,
        constructor: function(logged){
            this.loggedInVar = logged;
        },

        formGenerator: function(title, url, operation) {
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
                                if (operation == 'login')
                                {
                                    this.loggedInVar = true;
                                }
                                dialog.close();
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
                        dialog.close();
                    }
                }]
            });
            dialog = new Ext.Window({
                height: 140,
                width: 300,
                closable: true,
                closeAction : 'hide',
                modal: true,
                title: title,
                layout: 'fit',
                items: f
            });
            return dialog;
        },
        getLoggedInStatus: function() {
            return this.loggedInVar;
        },

        login: function(store) {
            loginDlg = this.formGenerator('Login','auth/', 'login');
            loginDlg.show();
            loginDlg.on('close', function(){store.reload()})
        },
        register: function() {
            registerDlg = this.formGenerator('Register','auth/', 'register');
            registerDlg.show();
        },
        logout: function(store) {
            Ext.Ajax.request({
                url: 'auth/',
                method: 'POST',
                params: {'operation': 'logout'},
                success: function(result, request) {
                    this.loggedInVar = false;
                    store.reload()
                }
            });
        }

    });
});