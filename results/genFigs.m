text = fileread('bleu_orig');
text = strsplit(text,'\n');

methodScores = cell(length(text)/4,2);
q = 1;
for i = 1:4:length(text)
    methodScores{q,1} = text{i};
    methodScores{q,2} = cellfun(@str2num,text(i+1:i+3));
    q=q+1;    
end


hold on
bar(cell2mat([methodScores(1:5,2)]));
set(gca,'XTick', 1:5, 'XTickLabel', methodScores(1:5));
legend('fold1','fold2','fold3')
xlabel('Method', 'FontSize', 20, 'FontWeight', 'bold')
ylabel('Score', 'FontSize', 20, 'FontWeight', 'bold')
set(gca,'FontSize',16, 'FontWeight','bold')