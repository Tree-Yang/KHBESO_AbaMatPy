%Function to plot iteration curves
%*******************************************************
%By J S Yang
%Date: 2018-12-05
%*******************************************************
function [DV,ObjVal] = HistoryPlot
    DV0 = load('./DesignVariables/DV_Iter0.dat');
    DVNum = length(DV0);
    IterNum = 0;

    % Number of files in folder: 'DesignVariables'
    FolderFile = dir('./DesignVariables');
    FolderFileNum = length(FolderFile);
    for ii = 1:1:FolderFileNum
        IterNum = IterNum + (1 - 1.0*FolderFile(ii).isdir);
    end

    DV = zeros(DVNum, IterNum);

    for ii = 1:1:IterNum
        FileName = ['.\DesignVariables\','DV_Iter',num2str(ii-1),'.dat'];
        DV(:,ii) = load(FileName);
    end

    ObjVal = load('ModelTotExtWork.dat');

    PlotN = min(length(ObjVal), IterNum);

    %Plot value fraction curve
    figure(1);
    plot(sum(DV)/DVNum,'LineWidth',1);
    grid on;
    xlabel('Iterations');
    ylabel('Volume Fraction')
    set(gca,'FontSize',12,'FontName','Euclid');
    figure(2);
    plot(ObjVal(1:PlotN),'LineWidth',1);
    grid on;
    xlabel('Iterations');
    ylabel('Objective Value')
    set(gca,'FontSize',12,'FontName','Euclid');
end