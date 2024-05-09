namespace MFLEX_Compass.UI
{
    partial class LoginForm
    {
        /// <summary>
        /// Required designer variable.
        /// </summary>
        private System.ComponentModel.IContainer components = null;

        /// <summary>
        /// Clean up any resources being used.
        /// </summary>
        /// <param name="disposing">true if managed resources should be disposed; otherwise, false.</param>
        protected override void Dispose(bool disposing)
        {
            if (disposing && (components != null))
            {
                components.Dispose();
            }
            base.Dispose(disposing);
        }

        #region Windows Form Designer generated code

        /// <summary>
        /// Required method for Designer support - do not modify
        /// the contents of this method with the code editor.
        /// </summary>
        private void InitializeComponent()
        {
            System.ComponentModel.ComponentResourceManager resources = new System.ComponentModel.ComponentResourceManager(typeof(LoginForm));
            this.label1 = new System.Windows.Forms.Label();
            this.cbRole = new System.Windows.Forms.ComboBox();
            this.cbFixtureId = new System.Windows.Forms.ComboBox();
            this.label2 = new System.Windows.Forms.Label();
            this.cbLineLvl = new System.Windows.Forms.ComboBox();
            this.label3 = new System.Windows.Forms.Label();
            this.cbLineId = new System.Windows.Forms.ComboBox();
            this.label4 = new System.Windows.Forms.Label();
            this.cbSerialNum = new System.Windows.Forms.ComboBox();
            this.label5 = new System.Windows.Forms.Label();
            this.cbProjectName = new System.Windows.Forms.ComboBox();
            this.label6 = new System.Windows.Forms.Label();
            this.cbWorkArea = new System.Windows.Forms.ComboBox();
            this.label7 = new System.Windows.Forms.Label();
            this.label8 = new System.Windows.Forms.Label();
            this.label9 = new System.Windows.Forms.Label();
            this.tableLayoutPanel1 = new System.Windows.Forms.TableLayoutPanel();
            this.tbOperator = new System.Windows.Forms.TextBox();
            this.tbPwd = new System.Windows.Forms.TextBox();
            this.tableLayoutPanel2 = new System.Windows.Forms.TableLayoutPanel();
            this.btLogin = new System.Windows.Forms.Button();
            this.btExit = new System.Windows.Forms.Button();
            this.tableLayoutPanel1.SuspendLayout();
            this.tableLayoutPanel2.SuspendLayout();
            this.SuspendLayout();
            // 
            // label1
            // 
            this.label1.Anchor = System.Windows.Forms.AnchorStyles.Left;
            this.label1.AutoSize = true;
            this.label1.Location = new System.Drawing.Point(3, 9);
            this.label1.Name = "label1";
            this.label1.Size = new System.Drawing.Size(90, 21);
            this.label1.TabIndex = 0;
            this.label1.Text = "用户模式：";
            // 
            // cbRole
            // 
            this.cbRole.Anchor = System.Windows.Forms.AnchorStyles.Left;
            this.cbRole.FormattingEnabled = true;
            this.cbRole.Items.AddRange(new object[] {
            "操作员",
            "技术员",
            "工程师"});
            this.cbRole.Location = new System.Drawing.Point(118, 5);
            this.cbRole.MinimumSize = new System.Drawing.Size(180, 0);
            this.cbRole.Name = "cbRole";
            this.cbRole.Size = new System.Drawing.Size(313, 29);
            this.cbRole.TabIndex = 1;
            // 
            // cbFixtureId
            // 
            this.cbFixtureId.Anchor = System.Windows.Forms.AnchorStyles.Left;
            this.cbFixtureId.FormattingEnabled = true;
            this.cbFixtureId.Location = new System.Drawing.Point(118, 44);
            this.cbFixtureId.MinimumSize = new System.Drawing.Size(180, 0);
            this.cbFixtureId.Name = "cbFixtureId";
            this.cbFixtureId.Size = new System.Drawing.Size(313, 29);
            this.cbFixtureId.TabIndex = 3;
            // 
            // label2
            // 
            this.label2.Anchor = System.Windows.Forms.AnchorStyles.Left;
            this.label2.AutoSize = true;
            this.label2.Location = new System.Drawing.Point(3, 48);
            this.label2.Name = "label2";
            this.label2.Size = new System.Drawing.Size(90, 21);
            this.label2.TabIndex = 2;
            this.label2.Text = "治具编号：";
            // 
            // cbLineLvl
            // 
            this.cbLineLvl.Anchor = System.Windows.Forms.AnchorStyles.Left;
            this.cbLineLvl.FormattingEnabled = true;
            this.cbLineLvl.Location = new System.Drawing.Point(118, 83);
            this.cbLineLvl.MinimumSize = new System.Drawing.Size(180, 0);
            this.cbLineLvl.Name = "cbLineLvl";
            this.cbLineLvl.Size = new System.Drawing.Size(313, 29);
            this.cbLineLvl.TabIndex = 5;
            // 
            // label3
            // 
            this.label3.Anchor = System.Windows.Forms.AnchorStyles.Left;
            this.label3.AutoSize = true;
            this.label3.Location = new System.Drawing.Point(3, 87);
            this.label3.Name = "label3";
            this.label3.Size = new System.Drawing.Size(58, 21);
            this.label3.TabIndex = 4;
            this.label3.Text = "线别：";
            // 
            // cbLineId
            // 
            this.cbLineId.Anchor = System.Windows.Forms.AnchorStyles.Left;
            this.cbLineId.FormattingEnabled = true;
            this.cbLineId.Location = new System.Drawing.Point(118, 122);
            this.cbLineId.MinimumSize = new System.Drawing.Size(180, 0);
            this.cbLineId.Name = "cbLineId";
            this.cbLineId.Size = new System.Drawing.Size(313, 29);
            this.cbLineId.TabIndex = 7;
            // 
            // label4
            // 
            this.label4.Anchor = System.Windows.Forms.AnchorStyles.Left;
            this.label4.AutoSize = true;
            this.label4.Location = new System.Drawing.Point(3, 126);
            this.label4.Name = "label4";
            this.label4.Size = new System.Drawing.Size(58, 21);
            this.label4.TabIndex = 6;
            this.label4.Text = "线体：";
            // 
            // cbSerialNum
            // 
            this.cbSerialNum.Anchor = System.Windows.Forms.AnchorStyles.Left;
            this.cbSerialNum.FormattingEnabled = true;
            this.cbSerialNum.Location = new System.Drawing.Point(118, 161);
            this.cbSerialNum.MinimumSize = new System.Drawing.Size(180, 0);
            this.cbSerialNum.Name = "cbSerialNum";
            this.cbSerialNum.Size = new System.Drawing.Size(313, 29);
            this.cbSerialNum.TabIndex = 9;
            // 
            // label5
            // 
            this.label5.Anchor = System.Windows.Forms.AnchorStyles.Left;
            this.label5.AutoSize = true;
            this.label5.Location = new System.Drawing.Point(3, 165);
            this.label5.Name = "label5";
            this.label5.Size = new System.Drawing.Size(58, 21);
            this.label5.TabIndex = 8;
            this.label5.Text = "料号：";
            // 
            // cbProjectName
            // 
            this.cbProjectName.Anchor = System.Windows.Forms.AnchorStyles.Left;
            this.cbProjectName.FormattingEnabled = true;
            this.cbProjectName.Location = new System.Drawing.Point(118, 200);
            this.cbProjectName.MinimumSize = new System.Drawing.Size(180, 0);
            this.cbProjectName.Name = "cbProjectName";
            this.cbProjectName.Size = new System.Drawing.Size(313, 29);
            this.cbProjectName.TabIndex = 11;
            // 
            // label6
            // 
            this.label6.Anchor = System.Windows.Forms.AnchorStyles.Left;
            this.label6.AutoSize = true;
            this.label6.Location = new System.Drawing.Point(3, 204);
            this.label6.Name = "label6";
            this.label6.Size = new System.Drawing.Size(58, 21);
            this.label6.TabIndex = 10;
            this.label6.Text = "项目：";
            // 
            // cbWorkArea
            // 
            this.cbWorkArea.Anchor = System.Windows.Forms.AnchorStyles.Left;
            this.cbWorkArea.FormattingEnabled = true;
            this.cbWorkArea.Location = new System.Drawing.Point(118, 239);
            this.cbWorkArea.MinimumSize = new System.Drawing.Size(180, 0);
            this.cbWorkArea.Name = "cbWorkArea";
            this.cbWorkArea.Size = new System.Drawing.Size(313, 29);
            this.cbWorkArea.TabIndex = 13;
            // 
            // label7
            // 
            this.label7.Anchor = System.Windows.Forms.AnchorStyles.Left;
            this.label7.AutoSize = true;
            this.label7.Location = new System.Drawing.Point(3, 243);
            this.label7.Name = "label7";
            this.label7.Size = new System.Drawing.Size(58, 21);
            this.label7.TabIndex = 12;
            this.label7.Text = "车间：";
            // 
            // label8
            // 
            this.label8.Anchor = System.Windows.Forms.AnchorStyles.Left;
            this.label8.AutoSize = true;
            this.label8.Location = new System.Drawing.Point(3, 282);
            this.label8.Name = "label8";
            this.label8.Size = new System.Drawing.Size(58, 21);
            this.label8.TabIndex = 14;
            this.label8.Text = "工号：";
            // 
            // label9
            // 
            this.label9.Anchor = System.Windows.Forms.AnchorStyles.Left;
            this.label9.AutoSize = true;
            this.label9.Location = new System.Drawing.Point(3, 323);
            this.label9.Name = "label9";
            this.label9.Size = new System.Drawing.Size(58, 21);
            this.label9.TabIndex = 16;
            this.label9.Text = "密码：";
            // 
            // tableLayoutPanel1
            // 
            this.tableLayoutPanel1.ColumnCount = 2;
            this.tableLayoutPanel1.ColumnStyles.Add(new System.Windows.Forms.ColumnStyle(System.Windows.Forms.SizeType.Percent, 26.4977F));
            this.tableLayoutPanel1.ColumnStyles.Add(new System.Windows.Forms.ColumnStyle(System.Windows.Forms.SizeType.Percent, 73.5023F));
            this.tableLayoutPanel1.Controls.Add(this.label1, 0, 0);
            this.tableLayoutPanel1.Controls.Add(this.cbRole, 1, 0);
            this.tableLayoutPanel1.Controls.Add(this.label2, 0, 1);
            this.tableLayoutPanel1.Controls.Add(this.cbFixtureId, 1, 1);
            this.tableLayoutPanel1.Controls.Add(this.label9, 0, 8);
            this.tableLayoutPanel1.Controls.Add(this.label3, 0, 2);
            this.tableLayoutPanel1.Controls.Add(this.cbLineLvl, 1, 2);
            this.tableLayoutPanel1.Controls.Add(this.label8, 0, 7);
            this.tableLayoutPanel1.Controls.Add(this.label4, 0, 3);
            this.tableLayoutPanel1.Controls.Add(this.cbWorkArea, 1, 6);
            this.tableLayoutPanel1.Controls.Add(this.cbLineId, 1, 3);
            this.tableLayoutPanel1.Controls.Add(this.label7, 0, 6);
            this.tableLayoutPanel1.Controls.Add(this.label5, 0, 4);
            this.tableLayoutPanel1.Controls.Add(this.cbProjectName, 1, 5);
            this.tableLayoutPanel1.Controls.Add(this.cbSerialNum, 1, 4);
            this.tableLayoutPanel1.Controls.Add(this.label6, 0, 5);
            this.tableLayoutPanel1.Controls.Add(this.tbOperator, 1, 7);
            this.tableLayoutPanel1.Controls.Add(this.tbPwd, 1, 8);
            this.tableLayoutPanel1.Location = new System.Drawing.Point(21, 12);
            this.tableLayoutPanel1.Name = "tableLayoutPanel1";
            this.tableLayoutPanel1.RowCount = 9;
            this.tableLayoutPanel1.RowStyles.Add(new System.Windows.Forms.RowStyle(System.Windows.Forms.SizeType.Percent, 11.11111F));
            this.tableLayoutPanel1.RowStyles.Add(new System.Windows.Forms.RowStyle(System.Windows.Forms.SizeType.Percent, 11.11111F));
            this.tableLayoutPanel1.RowStyles.Add(new System.Windows.Forms.RowStyle(System.Windows.Forms.SizeType.Percent, 11.11111F));
            this.tableLayoutPanel1.RowStyles.Add(new System.Windows.Forms.RowStyle(System.Windows.Forms.SizeType.Percent, 11.11111F));
            this.tableLayoutPanel1.RowStyles.Add(new System.Windows.Forms.RowStyle(System.Windows.Forms.SizeType.Percent, 11.11111F));
            this.tableLayoutPanel1.RowStyles.Add(new System.Windows.Forms.RowStyle(System.Windows.Forms.SizeType.Percent, 11.11111F));
            this.tableLayoutPanel1.RowStyles.Add(new System.Windows.Forms.RowStyle(System.Windows.Forms.SizeType.Percent, 11.11111F));
            this.tableLayoutPanel1.RowStyles.Add(new System.Windows.Forms.RowStyle(System.Windows.Forms.SizeType.Percent, 11.11111F));
            this.tableLayoutPanel1.RowStyles.Add(new System.Windows.Forms.RowStyle(System.Windows.Forms.SizeType.Percent, 11.11111F));
            this.tableLayoutPanel1.RowStyles.Add(new System.Windows.Forms.RowStyle(System.Windows.Forms.SizeType.Absolute, 20F));
            this.tableLayoutPanel1.Size = new System.Drawing.Size(434, 356);
            this.tableLayoutPanel1.TabIndex = 20;
            // 
            // tbOperator
            // 
            this.tbOperator.Anchor = System.Windows.Forms.AnchorStyles.Left;
            this.tbOperator.Location = new System.Drawing.Point(118, 278);
            this.tbOperator.Name = "tbOperator";
            this.tbOperator.Size = new System.Drawing.Size(313, 29);
            this.tbOperator.TabIndex = 17;
            this.tbOperator.KeyPress += new System.Windows.Forms.KeyPressEventHandler(this.tbOperator_KeyPress);
            // 
            // tbPwd
            // 
            this.tbPwd.Anchor = System.Windows.Forms.AnchorStyles.Left;
            this.tbPwd.Location = new System.Drawing.Point(118, 319);
            this.tbPwd.Name = "tbPwd";
            this.tbPwd.PasswordChar = '*';
            this.tbPwd.Size = new System.Drawing.Size(313, 29);
            this.tbPwd.TabIndex = 18;
            this.tbPwd.KeyPress += new System.Windows.Forms.KeyPressEventHandler(this.tbPwd_KeyPress);
            // 
            // tableLayoutPanel2
            // 
            this.tableLayoutPanel2.ColumnCount = 2;
            this.tableLayoutPanel2.ColumnStyles.Add(new System.Windows.Forms.ColumnStyle(System.Windows.Forms.SizeType.Percent, 50F));
            this.tableLayoutPanel2.ColumnStyles.Add(new System.Windows.Forms.ColumnStyle(System.Windows.Forms.SizeType.Percent, 50F));
            this.tableLayoutPanel2.Controls.Add(this.btLogin, 0, 0);
            this.tableLayoutPanel2.Controls.Add(this.btExit, 1, 0);
            this.tableLayoutPanel2.Location = new System.Drawing.Point(21, 374);
            this.tableLayoutPanel2.Name = "tableLayoutPanel2";
            this.tableLayoutPanel2.RowCount = 1;
            this.tableLayoutPanel2.RowStyles.Add(new System.Windows.Forms.RowStyle(System.Windows.Forms.SizeType.Percent, 100F));
            this.tableLayoutPanel2.RowStyles.Add(new System.Windows.Forms.RowStyle(System.Windows.Forms.SizeType.Absolute, 54F));
            this.tableLayoutPanel2.Size = new System.Drawing.Size(434, 54);
            this.tableLayoutPanel2.TabIndex = 21;
            // 
            // btLogin
            // 
            this.btLogin.Anchor = System.Windows.Forms.AnchorStyles.Left;
            this.btLogin.AutoSize = true;
            this.btLogin.Location = new System.Drawing.Point(3, 8);
            this.btLogin.Name = "btLogin";
            this.btLogin.Size = new System.Drawing.Size(211, 38);
            this.btLogin.TabIndex = 0;
            this.btLogin.Text = "登录";
            this.btLogin.UseVisualStyleBackColor = true;
            this.btLogin.Click += new System.EventHandler(this.btLogin_Click);
            // 
            // btExit
            // 
            this.btExit.Anchor = System.Windows.Forms.AnchorStyles.Left;
            this.btExit.AutoSize = true;
            this.btExit.Location = new System.Drawing.Point(220, 8);
            this.btExit.Name = "btExit";
            this.btExit.Size = new System.Drawing.Size(211, 38);
            this.btExit.TabIndex = 1;
            this.btExit.Text = "退出";
            this.btExit.UseVisualStyleBackColor = true;
            this.btExit.Click += new System.EventHandler(this.btExit_Click);
            // 
            // LoginForm
            // 
            this.AutoScaleDimensions = new System.Drawing.SizeF(10F, 21F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.BackColor = System.Drawing.Color.White;
            this.ClientSize = new System.Drawing.Size(470, 444);
            this.Controls.Add(this.tableLayoutPanel2);
            this.Controls.Add(this.tableLayoutPanel1);
            this.Font = new System.Drawing.Font("微软雅黑", 12F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(134)));
            this.Icon = ((System.Drawing.Icon)(resources.GetObject("$this.Icon")));
            this.Margin = new System.Windows.Forms.Padding(5);
            this.Name = "LoginForm";
            this.Text = "用户登录";
            this.Load += new System.EventHandler(this.LoginForm_Load);
            this.tableLayoutPanel1.ResumeLayout(false);
            this.tableLayoutPanel1.PerformLayout();
            this.tableLayoutPanel2.ResumeLayout(false);
            this.tableLayoutPanel2.PerformLayout();
            this.ResumeLayout(false);

        }

        #endregion

        private System.Windows.Forms.Label label1;
        private System.Windows.Forms.ComboBox cbRole;
        private System.Windows.Forms.ComboBox cbFixtureId;
        private System.Windows.Forms.Label label2;
        private System.Windows.Forms.ComboBox cbLineLvl;
        private System.Windows.Forms.Label label3;
        private System.Windows.Forms.ComboBox cbLineId;
        private System.Windows.Forms.Label label4;
        private System.Windows.Forms.ComboBox cbSerialNum;
        private System.Windows.Forms.Label label5;
        private System.Windows.Forms.ComboBox cbProjectName;
        private System.Windows.Forms.Label label6;
        private System.Windows.Forms.ComboBox cbWorkArea;
        private System.Windows.Forms.Label label7;
        private System.Windows.Forms.Label label8;
        private System.Windows.Forms.Label label9;
        private System.Windows.Forms.TableLayoutPanel tableLayoutPanel1;
        private System.Windows.Forms.TextBox tbOperator;
        private System.Windows.Forms.TextBox tbPwd;
        private System.Windows.Forms.TableLayoutPanel tableLayoutPanel2;
        private System.Windows.Forms.Button btLogin;
        private System.Windows.Forms.Button btExit;
    }
}