namespace MFLEX_Compass.UI
{
    partial class SettleConfig
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
            this.dgvSettleConfig = new System.Windows.Forms.DataGridView();
            this.btSave = new System.Windows.Forms.Button();
            this.SecName = new System.Windows.Forms.DataGridViewTextBoxColumn();
            this.KeyName = new System.Windows.Forms.DataGridViewTextBoxColumn();
            this.ValueName = new System.Windows.Forms.DataGridViewTextBoxColumn();
            ((System.ComponentModel.ISupportInitialize)(this.dgvSettleConfig)).BeginInit();
            this.SuspendLayout();
            // 
            // dgvSettleConfig
            // 
            this.dgvSettleConfig.AutoSizeColumnsMode = System.Windows.Forms.DataGridViewAutoSizeColumnsMode.Fill;
            this.dgvSettleConfig.ColumnHeadersHeightSizeMode = System.Windows.Forms.DataGridViewColumnHeadersHeightSizeMode.AutoSize;
            this.dgvSettleConfig.Columns.AddRange(new System.Windows.Forms.DataGridViewColumn[] {
            this.SecName,
            this.KeyName,
            this.ValueName});
            this.dgvSettleConfig.Location = new System.Drawing.Point(27, 24);
            this.dgvSettleConfig.Name = "dgvSettleConfig";
            this.dgvSettleConfig.RowTemplate.Height = 23;
            this.dgvSettleConfig.Size = new System.Drawing.Size(511, 269);
            this.dgvSettleConfig.TabIndex = 0;
            // 
            // btSave
            // 
            this.btSave.Font = new System.Drawing.Font("微软雅黑", 12F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(134)));
            this.btSave.Location = new System.Drawing.Point(27, 299);
            this.btSave.Name = "btSave";
            this.btSave.Size = new System.Drawing.Size(511, 36);
            this.btSave.TabIndex = 1;
            this.btSave.Text = "保存";
            this.btSave.UseVisualStyleBackColor = true;
            this.btSave.Click += new System.EventHandler(this.btSave_Click);
            // 
            // SecName
            // 
            this.SecName.HeaderText = "参数节点";
            this.SecName.MinimumWidth = 20;
            this.SecName.Name = "SecName";
            this.SecName.ReadOnly = true;
            // 
            // KeyName
            // 
            this.KeyName.HeaderText = "参数名";
            this.KeyName.MinimumWidth = 20;
            this.KeyName.Name = "KeyName";
            this.KeyName.ReadOnly = true;
            // 
            // ValueName
            // 
            this.ValueName.HeaderText = "参数值";
            this.ValueName.MinimumWidth = 20;
            this.ValueName.Name = "ValueName";
            // 
            // SettleConfig
            // 
            this.AutoScaleDimensions = new System.Drawing.SizeF(7F, 17F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.ClientSize = new System.Drawing.Size(565, 347);
            this.Controls.Add(this.btSave);
            this.Controls.Add(this.dgvSettleConfig);
            this.Font = new System.Drawing.Font("微软雅黑", 9F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(134)));
            this.Margin = new System.Windows.Forms.Padding(4, 4, 4, 4);
            this.Name = "SettleConfig";
            this.Text = "SettleConfig";
            this.Load += new System.EventHandler(this.SettleConfig_Load);
            ((System.ComponentModel.ISupportInitialize)(this.dgvSettleConfig)).EndInit();
            this.ResumeLayout(false);

        }

        #endregion

        private System.Windows.Forms.DataGridView dgvSettleConfig;
        private System.Windows.Forms.Button btSave;
        private System.Windows.Forms.DataGridViewTextBoxColumn SecName;
        private System.Windows.Forms.DataGridViewTextBoxColumn KeyName;
        private System.Windows.Forms.DataGridViewTextBoxColumn ValueName;
    }
}