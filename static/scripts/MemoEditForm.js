Ext.onReady(function(){
    Ext.define("My.scripts.MemoEditForm", {
        memoEditDlg: "None",
        constructor: function (id) {
            console.log('before in constructor');
            f = new Ext.FormPanel({
                labelWidth: 100,
                url: 'note/api/',
                frame: true,
                defaults: {width: 100},

                items: [
                    {
                        xtype: 'hidden',
                        fieldLabel: 'Id',
                        name: 'id',
                        value: id
                    },
                    {
                        xtype: 'textfield',
                        fieldLabel: 'Title',
                        name: 'title',
                        editable: false,
                        allowBlank: false
                    },{
                        xtype: 'htmleditor',
                        fieldLabel: 'Text',
                        name: 'text',
                        hideLabel: true,
                        allowBlank: false,
                        anchor: '100%',
                    },{
                        xtype: 'checkbox',
                        fieldLabel: 'Chosen',
                        name: 'chosen',
                        type: 'boolean',
                        anchor: '50%',
                    },{
                        xtype: 'checkbox',
                        fieldLabel: 'Published',
                        name: 'published',
                        type: 'boolean',
                        anchor: '50%',
                    }
                ],
                buttons: [{
                    text: 'OK',
                    minWidth: 75,
                    handler: function() {
                        f.getForm().submit(
                            {
                            success: function(form, action){
                                //Ext.Msg.alert('Success', 'It worked');
                                memoEditDlg.close();
                            },
                            failure: function(form, action){
                                Ext.Msg.alert('Warning', action.result.errormsg);
                            }
                        });
                    }
                },

                {
                    text: 'Cancel',
                    minWidth: 75,
                    handler: function() {
                        memoEditDlg.close();
                    }
                }]
            });
            if (id != undefined){
                f.getForm().load({
                    params:{id:id, operation: 'read'},
                    waitMsg: 'Loading'
                });
            }
            console.log('f created');
            memoEditDlg = new Ext.Window({
                height: 400,
                width: 300,
                closable: true,
                closeAction : 'hide',
                modal: true,
                title: 'Memo',
                layout: 'fit',
                items: f
            });

            memoEditDlg.show();
            this.memoEditDlg = memoEditDlg;

        }
    });
    //var bom = new My.scripts.MemoEditForm();
});